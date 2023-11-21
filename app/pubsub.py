
import os
from flask import Flask
from src.models import db
from dotenv import load_dotenv
import traceback
from src.tasks import convert_video
import uuid
from google.cloud import pubsub_v1
import json
from google.auth import jwt

load_dotenv()

app = Flask(__name__)

    # Load configuration from a .env file
load_dotenv()

# Configure the database
db.init_app(app)


topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    topic='worker-topic',  # Set this to something appropriate.
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    sub='worker-pubsub'+str(uuid.uuid4()),  # Set this to something appropriate.
)

def callback(message):
    print(message.data)
    input = message.data
    print(input)
    print(type(input))
    inputJson = json.loads(input)
    print(inputJson)
    print(type(inputJson))

    try:
        convert_video(inputJson.get("task_id"), inputJson.get("input_url"), inputJson.get("output_format"))
    except:
        traceback.print_exc()
    
    message.ack()

with pubsub_v1.SubscriberClient() as subscriber:
    subscriber.create_subscription(
        name=subscription_name, topic=topic_name)
    future = subscriber.subscribe(subscription_name, callback)

    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()