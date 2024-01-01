from logging import getLogger, LoggerAdapter
from uuid import UUID

from originations.middleware.context import get_request_id

logger = getLogger("loans-originations")


class CustomLoggerAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        # Add request_id to the log record
        kwargs["extra"] = {"request_id": get_request_id()}
        return msg, kwargs


def get_logger():
    return CustomLoggerAdapter(logger, {})
