import asyncio
import logging
from originations.models.credit_variables import CreditVariables
from originations.models.application import ApplicationRequest


async def mock_risk_model_service(
    request: ApplicationRequest, credit_variables: CreditVariables
):
    logger = logging.getLogger("api-logger")
    await asyncio.sleep(0.5)

    risk_score = (750 - credit_variables.credit_score) / 500

    logger.info(f"Scored application with a risk score of {risk_score}")

    return risk_score
