from google.cloud import pubsub_v1
from myconfig import MyConfig
import os

config = MyConfig(['settings.json', '.secrets.json'])
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.pubsub_admin_key_path

project_id = config.project_id
topic_id = config.topic_id

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

if __name__ == "__main__":
    topic = publisher.create_topic(request={"name": topic_path})

    print(f"Created topic: {topic.name}")