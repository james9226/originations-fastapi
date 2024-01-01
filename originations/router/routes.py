from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from originations.dependancies.auth import get_current_username

from originations.models.request import ApplicationRequestInput
from originations.models.submission_request import SubmissionRequest
from originations.quoter.orchestrator import orchestrator
from originations.resumer.handler import handle_resuming_application_by_application_id
from originations.services.cloudsql.initialize import get_db


v1_router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    # dependencies=[Depends(verify_pubsub_token)],
    responses={404: {"description": "Not found"}},
)


## Application Endpoint
@v1_router.post("/application/")
async def application(
    request: ApplicationRequestInput,
    username: str = Depends(get_current_username),
    db: AsyncSession = Depends(get_db),
):
    result = await orchestrator(request, db)
    return result


@v1_router.get("/application/{id}")
async def get_application_by_id(
    id: UUID,
    username: str = Depends(get_current_username),
    db: AsyncSession = Depends(get_db),
):
    return await handle_resuming_application_by_application_id(id, db)


## Submission Endpoint
@v1_router.post("/submission/")
async def submission(
    request: SubmissionRequest, username: str = Depends(get_current_username)
):
    return JSONResponse(
        content={"status_code": 10200, "message": "Application Approved", "data": None},
        status_code=status.HTTP_200_OK,
    )
