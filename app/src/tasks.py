import os
from moviepy.editor import VideoFileClip
from flask import current_app
import config
import requests
from .models import db, Task
from celery import shared_task
import config
from google.cloud import storage

def convert_video(task_id, input_url, output_format):
    try:
        #task = Task.query.get(task_id)
        print("Input URL", input_url, flush=True)

        # Update the task status to 'processing'
        #task.status = 'processing'
        #db.session.commit()

        # Download the video file from the URL
        response = requests.get(input_url, stream=True)
        response.raise_for_status()

        # Perform the video conversion
        input_path = os.path.join(os.getcwd(), config.UPLOAD_FOLDER, f"{task_id}_input.{output_format}")
        output_path = os.path.join(os.getcwd(), config.OUTPUT_FOLDER, f"{task_id}_output.{output_format}")
        
        with open(input_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        # Convert the video format
        clip = VideoFileClip(input_path)
        clip.write_videofile(output_path)

        # Update the task status to 'processed'
        #task.status = 'processed'
        #db.session.commit()

        # Upload the converted file to GCP bucket
        upload_to_gcp_bucket(task_id, output_path, output_format)

    except Exception as e:
        # Handle any exceptions and set the task status to 'failed'
        #task.status = 'failed'
        #db.session.commit()
        raise e



def upload_to_gcp_bucket(task_id, file_path, output_format):
    project_id = config.GOOGLE_CLOUD_PROJECT
    bucket_name = config.GOOGLE_CLOUD_BUCKET
    credentials_path = config.GOOGLE_CLOUD_CREDENTIALS_PATH

    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)

    blob_name = f"{task_id}_output.{output_format}"
    blob = bucket.blob(blob_name)

    # Upload the file to GCP bucket
    blob.upload_from_filename(file_path)

    # Delete the local file after uploading to GCP
    os.remove(file_path)