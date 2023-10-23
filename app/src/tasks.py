import os
from moviepy.editor import VideoFileClip
from flask import current_app
from .models import db, Task
from celery import shared_task


@shared_task(ignore_result=False)
def convert_video(task_id, input_file, output_format):
    try:
        task = Task.query.get(task_id)

        # Update the task status to 'processing'
        task.status = 'processing'
        db.session.commit()

        # Perform the video conversion
        input_path = os.path.join(current_app.config['UPLOAD_FOLDER'], input_file)
        output_file = f"{task_id}.{output_format}"
        output_path = os.path.join(current_app.config['OUTPUT_FOLDER'], output_file)

        clip = VideoFileClip(input_path)
        clip.write_videofile(output_path + '.' + output_format)

        # Update the task status to 'processed'
        task.status = 'processed'
        db.session.commit()
    except Exception as e:
        # Handle any exceptions and set the task status to 'failed'
        task.status = 'failed'
        db.session.commit()
        raise e

