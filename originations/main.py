import logging
import secrets
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from logging.config import dictConfig
from originations.middleware.context import RequestContextMiddleware
from originations.models.request import ApplicationRequestInput
from originations.domain.application_orchestrator import application_orchestrator
from originations.models.submission_request import SubmissionRequest
from originations.services.logging.config import log_config
from originations.services.secretsmanager.secrets import access_secret_version
from originations.config.config import settings

dictConfig(log_config)

app = FastAPI(
    title="Originations with FastAPI",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    debug=True,
)

logger = logging.getLogger("api-logger")

app.add_middleware(RequestContextMiddleware)


## Initial Basic Auth
security = HTTPBasic()


## For document
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user")
    correct_password = secrets.compare_digest(
        credentials.password, access_secret_version("originations-api-key")
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(exc)
    content = {"status_code": 10400, "message": exc_str, "data": None}
    return JSONResponse(content=content, status_code=status.HTTP_400_BAD_REQUEST)


## Create Auth Doc
@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.post("/v1/application/")
async def application(
    request: ApplicationRequestInput, username: str = Depends(get_current_username)
):
    print("Project id:", settings.project_id)
    result = await application_orchestrator(request)
    return result


@app.post("/v1/submission/")
async def submission(
    request: SubmissionRequest, username: str = Depends(get_current_username)
):
    return JSONResponse(
        content={"status_code": 10200, "message": "Application Approved", "data": None},
        status_code=status.HTTP_200_OK,
    )
