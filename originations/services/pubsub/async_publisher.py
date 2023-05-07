import datetime
import json
from google.cloud import pubsub_v1
import fastavro
from io import BytesIO
from originations.services.logging import log_handler

pubsub_publisher = pubsub_v1.PublisherClient()


def serialize_avro(record, schema):
    bytes_writer = BytesIO()
    fastavro.schemaless_writer(bytes_writer, schema, record)
    return bytes_writer.getvalue()


async def push_to_pubsub(topic_path, record, avro_schema):
    avro_binary = serialize_avro(record, avro_schema)

    # Create a future object to wait for the publish result
    future = pubsub_publisher.publish(topic_path, avro_binary)

    # Add a callback to get the result of the publish operation
    def callback(future):
        try:
            pass
        except Exception as e:
            log_handler.error(f"An error occurred when publishing the message: {e}")

    future.add_done_callback(callback)
