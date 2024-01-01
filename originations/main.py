import logging
from logging.config import dictConfig

from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from originations.dependancies.auth import get_current_username

from originations.middleware.context import RequestContextMiddleware
from originations.services.cloudsql.initialize import (
    close_cloudsql_pool,
    drop_db,
    heartbeat,
    initialize_cloudsql,
)
from originations.services.cloudsql.migrate import perform_cloudsql_migration
from originations.services.logging.config import log_config
from originations.router.routes import v1_router

# Dictionary Config for our Logging!
dictConfig(log_config)

# Create the FastAPI App!
app = FastAPI(
    title="Originations with FastAPI",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    debug=True,
)

logger = logging.getLogger("api-logger")


@app.on_event("startup")
async def perform_setup():
    # await initialize_cloudsql_proxy_connection()
    await initialize_cloudsql()
    await heartbeat()
    # await drop_db()
    # await perform_cloudsql_migration()
    # await seed_db()
    # initialize_pub_sub_publisher(settings.project_id, logger)


@app.on_event("shutdown")
async def shutdown():
    await close_cloudsql_pool()


# This middleware attatches context IDs, as well as providing before and after logging
# Middlewares run async, so we need the middleware that provides context IDs
# to also do the before/after logging, otherwise the logging will not have access to the context IDs!
app.add_middleware(RequestContextMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(exc)
    content = {"status_code": 10400, "message": exc_str, "data": None}
    return JSONResponse(content=content, status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


## Docs Endpoint
@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


app.include_router(v1_router)
