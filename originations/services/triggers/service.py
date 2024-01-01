from datetime import datetime
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from originations.models.past_triggers import PastPolicyTrigger

from originations.models.sqlmodels import ApplicationTriggers


class TriggersService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def query_triggers_by_hash(
        self, applicant_hash: str, min_timestamp: datetime
    ) -> list[ApplicationTriggers]:
        query = select(ApplicationTriggers).where(
            ApplicationTriggers.applicant_hash == applicant_hash,
            ApplicationTriggers.event_time >= min_timestamp,
        )
        applicants = await self.db.exec(query)
        return applicants.all()

    async def get_active_triggers_by_hash(
        self, applicant_hash: str, min_timestamp: datetime
    ) -> list[PastPolicyTrigger]:
        all_past_declines = await self.query_triggers_by_hash(
            applicant_hash, min_timestamp
        )

        return [
            PastPolicyTrigger(
                rule=code, phase=past_decline.phase, event_time=past_decline.event_time
            )
            for past_decline in all_past_declines
            for code in past_decline.triggered_codes
        ]

    async def save_triggers(
        self, application_id: UUID, applicant_hash: str, triggers: list[str]
    ) -> None:
        application_triggers = ApplicationTriggers(
            id=application_id,
            event_time=datetime.now(),
            applicant_hash=applicant_hash,
            triggers=triggers,
        )

        self.db.add(application_triggers)
