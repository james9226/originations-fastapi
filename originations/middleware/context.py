from contextvars import ContextVar
from logging import LoggerAdapter, getLogger
from typing import Optional
from uuid import uuid4, UUID
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request


BASE_LOGGER = getLogger("api-logger")


class SetLoggingAdapter(LoggerAdapter):
    def __init__(self, logger, request_id: UUID):
        super().__init__(logger, {})
        self.request_id = request_id

    def process(self, msg, kwargs):
        kwargs["extra"] = {"request_id": self.request_id}
        return msg, kwargs


REQUEST_ID_CTX_KEY = "request_id"
REQUEST_DATETIME_CTX_KEY = "request_datetime"

_request_id_ctx_key: ContextVar[Optional[UUID]] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None
)

_request_datetime_ctx_key: ContextVar[Optional[datetime]] = ContextVar(
    REQUEST_DATETIME_CTX_KEY, default=None
)


def get_request_id() -> Optional[UUID]:
    return _request_id_ctx_key.get()


def get_request_datetime() -> Optional[datetime]:
    return _request_datetime_ctx_key.get()


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # request_id = _request_id_ctx_key.set(str(uuid4()))
        request_id = _request_id_ctx_key.set(uuid4())

        request_datetime = _request_datetime_ctx_key.set(datetime.now())

        logger = SetLoggingAdapter(BASE_LOGGER, get_request_id())

        logger.info(f"start request path={request.url.path}")

        response = await call_next(request)

        process_time = (datetime.now() - get_request_datetime()) * 1000  # type: ignore[operator]

        # formatted_process_time = "{0:.2f}".format(str(process_time))

        logger.info(
            f"completed_in={process_time.total_seconds()}ms status_code={response.status_code}"
        )

        _request_id_ctx_key.reset(request_id)
        _request_datetime_ctx_key.reset(request_datetime)

        return response
