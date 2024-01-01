from uuid import UUID
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from originations.services.decision.service import DecisionService


async def handle_resuming_application_by_application_id(
    application_id: UUID, db: AsyncSession
) -> JSONResponse:
    decision_service = DecisionService(db)

    application = await decision_service.get_application_by_id(application_id)

    if application:
        return decision_service.build_response(application)

    return JSONResponse({"message": "not found"}, status_code=status.HTTP_404_NOT_FOUND)
