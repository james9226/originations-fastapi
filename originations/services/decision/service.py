from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import status
from fastapi.responses import JSONResponse

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from originations.enums.policy import PolicyOutcome

from originations.models.sqlmodels import ApplicationDecision, Quote
from originations.services.logging.log_handler import get_logger

logger = get_logger()


class DecisionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_application_by_id(
        self, application_id: UUID
    ) -> Optional[ApplicationDecision]:
        query = select(ApplicationDecision).where(
            ApplicationDecision.id == application_id
        )
        application = await self.db.exec(query)
        return application.first()

    async def get_applications_by_customer_id(
        self, customer_id: UUID, min_timestamp: datetime
    ) -> list[ApplicationDecision]:
        query = select(ApplicationDecision).where(
            ApplicationDecision.customer_id == customer_id,
            ApplicationDecision.event_time >= min_timestamp,
        )
        applications = await self.db.exec(query)
        return applications.all()

    def create_decision(
        self,
        application_id: UUID,
        decision: PolicyOutcome,
        reason: str,
        applicant_id: Optional[UUID],
        credit_profile_id: Optional[UUID],
        quotes: list[Quote] = [],
    ) -> ApplicationDecision:
        decision = ApplicationDecision(
            id=application_id,
            event_time=datetime.now(),
            decision=decision,
            reason=reason,
            applicant_id=applicant_id,
            credit_profile_id=credit_profile_id,
            quotes=quotes,
        )

        return decision

    async def save_decision(self, decision: ApplicationDecision) -> None:
        self.db.add(decision)

        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            logger.critical(
                f"Critical error while logging {decision.decision} due to {decision.reason} for application due to: {e}"
            )
            raise

        return decision

    def build_response(self, decision: ApplicationDecision) -> JSONResponse:
        match decision.decision:
            case PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR:
                return JSONResponse(
                    content={
                        "decision": PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
                        "id": str(decision.id),
                        "quotes": [],
                    },
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            case PolicyOutcome.REFERRED_DUE_TO_TECHNICAL_ERROR:
                return JSONResponse(
                    content={
                        "decision": PolicyOutcome.REFERRED,
                        "id": str(decision.id),
                        "quotes": [],
                    },
                    status_code=status.HTTP_200_OK,
                )

            case PolicyOutcome.PASSED:
                return JSONResponse(
                    content={
                        "decision": PolicyOutcome.PASSED,
                        "id": str(decision.id),
                        "quotes": decision.quotes,
                    },
                    status_code=status.HTTP_200_OK,
                )

            case _:
                return JSONResponse(
                    content={
                        "decision": decision.decision,
                        "id": str(decision.id),
                        "quotes": [],
                    },
                    status_code=status.HTTP_200_OK,
                )
