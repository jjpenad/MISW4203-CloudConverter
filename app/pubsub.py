
import os
from dotenv import load_dotenv
from src.tasks import convert_video
import uuid
from google.cloud import pubsub_v1
import json
from google.auth import jwt

load_dotenv()

#service_account_info = json.load(open(os.getenv('GOOGLE_CLOUD_CREDENTIALS_PATH')))
#service_account_file = os.getenv('GOOGLE_CLOUD_CREDENTIALS_PATH')
#audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"

#credentials = jwt.Credentials.from_service_account_file(
#        filename=service_account_file,
#)

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
    except Exception as e:
        print("ERROR CONVERTING", input)
        print("ERROR CONVERTING", e)
    
    message.ack()

with pubsub_v1.SubscriberClient() as subscriber:
    subscriber.create_subscription(
        name=subscription_name, topic=topic_name)
    future = subscriber.subscribe(subscription_name, callback)

    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()