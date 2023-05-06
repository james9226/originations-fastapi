from google.cloud import pubsub_v1
from originations.config.config import settings

publisher = pubsub_v1.PublisherClient()


async def publish_message_async(
    data: str, topic_id: str, project_id: str = settings.project_id
):
    topic_path = publisher.topic_path(project_id, topic_id)

    def _callback(future):
        try:
            print(f"Published message: {future.result()}")
        except Exception as e:
            print(f"An error occurred: {e}")

    data_as_bytes = data.encode("utf-8")
    future = publisher.publish(topic_path, data_as_bytes)
    future.add_done_callback(_callback)
