import asyncio
from datetime import datetime
import json
from typing import Any, Optional
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.types import BatchSettings

from originations.services.logging.log_handler import get_logger
from originations.config.config import settings


logger = get_logger()


class PubSubPublisherService:
    def __init__(
        self,
        project_id: str = settings.project_id,
        publisher: PublisherClient = PublisherClient(),
        batch_publisher: PublisherClient = PublisherClient(BatchSettings()),
    ):
        self.publisher = publisher
        self.batch_publisher = batch_publisher
        self.project_id = project_id

    @staticmethod
    def get_callback(future, data):
        def callback(future):
            try:
                pass
            except Exception as e:
                logger.critical(f"Publishing {data} raised an exception: {e}")

        return callback

    async def publish_message(self, message_dict: dict, topic_id: str) -> None:
        topic_path = self.publisher.topic_path(self.project_id, topic_id)

        # Encode the message as a JSON string
        message_dict["event_time"] = (
            datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        )

        message_json = json.dumps(message_dict).encode("utf-8")
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(
            None, self.publisher.publish, topic_path, message_json
        )
        future.add_done_callback(self.get_callback(future, message_json))

        # Wait for the message to be sent
        await future

    async def publish_batch_messages(
        self, message_dict_list: list[dict], topic_id: str
    ) -> None:
        topic_path = self.publisher.topic_path(self.project_id, topic_id)

        # Encode the messages as JSON strings
        message_json_list = [
            json.dumps(
                msg
                | {
                    "event_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[
                        :-3
                    ]
                    + "Z"
                }
            ).encode("utf-8")
            for msg in message_dict_list
        ]

        futures = []
        loop = asyncio.get_event_loop()
        for message_data in message_json_list:
            future = loop.run_in_executor(
                None, self.batch_publisher.publish, topic_path, message_data
            )
            future.add_done_callback(self.get_callback(future, message_data))
            futures.append(future)

        # Wait for all messages to be sent
        await asyncio.gather(*futures)
