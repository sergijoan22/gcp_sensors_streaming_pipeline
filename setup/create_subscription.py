from google.cloud import pubsub_v1
from myconfig import MyConfig
import os

config = MyConfig(['settings.json', '.secrets.json'])
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.pubsub_admin_key_path

project_id = config.project_id
topic_id = config.topic_id
subscription_id = config.subscription_id

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# create a pull subscription
with subscriber:
    subscription = subscriber.create_subscription(
        request={"name": subscription_path, "topic": topic_path}
    )

print(f"Subscription created: {subscription}")