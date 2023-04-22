import asyncio
from originations.domain.credit_variables.credit_variable_calculator import (
    calculate_credit_variables,
)
from originations.middleware.context import get_request_datetime, get_request_id
from originations.models.request import ApplicationRequestInput
from originations.models.application import ApplicationRequest
from originations.services.bureau.equifax.load_file import mock_equifax_request
from originations.services.firestore.io import post_event
from originations.domain.applicant_hash.hasher import hash_application
from originations.domain.outcomes.phase_outcomes import phase_outcome_decider
from originations.domain.outcomes.result import application_result
from originations.domain.policy.config.prevetting import CONFIG
from originations.domain.policy.policy_rules_runner import run_policy_rules
from originations.services.scorecard.risk_model_service import mock_risk_model_service


async def application_orchestrator(raw_request: ApplicationRequestInput):
    """
    - Validate Inputs

    Async:
        - Log Request to DB
        - Run Prevetting

    Async:
        - Log Prevetting Results to DB
        - Pull External Data

    Async:
        - Run Models
        - Run Quote Policy

    Async:
        - Log Models/Quote Outcomes
        - Run Application Policy

    Async:
        - Log Application Policy
        - Log Final Outcome

    Return Outcome


    """
    hash = hash_application(raw_request)

    request = ApplicationRequest(
        application_id=get_request_id(),
        event_time=get_request_datetime(),
        applicant_hash=hash,
        **raw_request.dict()
    )

    prevetting_policy_outcome, _ = await asyncio.gather(
        run_policy_rules(CONFIG, request.application_id, request=request),
        post_event("application_requests", str(request.application_id), request.dict()),
    )

    if phase_outcome_decider(prevetting_policy_outcome, "prevetting"):
        return application_result(prevetting_policy_outcome)

    credit_file = await mock_equifax_request(request)

    credit_variables = await calculate_credit_variables(credit_file)

    risk_score = await mock_risk_model_service(request, credit_variables)

    return application_result(prevetting_policy_outcome)
