from datetime import datetime, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from originations.enums.policy import PolicyOutcome


from originations.middleware.context import get_request_datetime, get_request_id
from originations.models.exceptions import (
    DeclinedException,
    ServiceCallFailure,
    UnexpectedError,
)
from originations.models.request import ApplicationRequestInput
from originations.services.applicant.service import ApplicantService
from originations.services.pubsub.service import PubSubPublisherService
from originations.services.triggers.service import TriggersService


async def orchestrator(request: ApplicationRequestInput, db: AsyncSession):
    # Save applicant to DB

    application_id, event_time = get_request_id(), get_request_datetime()
    if not application_id or not event_time:
        raise RuntimeError

    pubsub = PubSubPublisherService()

    applicant_service = ApplicantService(db)
    applicant = await applicant_service.create_applicant(request)

    triggers_service = TriggersService(db)
    past_triggers = await triggers_service.get_active_triggers_by_hash(
        applicant.applicant_hash, datetime.now() - timedelta(days=180)
    )

    await DeclinedException(
        "Unfinished!",
        db,
        application_id,
        applicant.id,
        None,
        PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
        "Not yet finished working on this lol",
    ).raise_with_db_save()

    # Run prevetting

    # Get Credit File

    # Calculate Variables

    # Run Credit File Rules

    # Generate Quotes

    # Run Risk Scorecard

    # Run Pricing

    # Run Affordability

    # Run Risk Score Rules

    # Return
