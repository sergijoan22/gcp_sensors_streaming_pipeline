from google.cloud import pubsub_v1
from myconfig import MyConfig
import os
from concurrent.futures import TimeoutError
import struct   # to convert bytes coming from Pub/Sub to float


# CONFIGURE PUBSUB
config = MyConfig(['settings.json', '.secrets.json'])
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.pubsub_admin_key_path


project_id = config.project_id
subscription_id = config.subscription_id
timeout = 5.0   # seconds to read be reading messages


subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


# function for dealing with messages
def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    message_show = {}
    message_show['value'] = float(message.data)    # read the data
    
    # read the attributes
    for key in message.attributes:
        message_show[key] = message.attributes.get(key)
    
    print(message_show)   # print the message
    message.ack()   # acknowledge the message to the topic

# read the topic
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")


with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.