import asyncio
from originations.models.application import ApplicationRequest
from originations.domain.policy.phase_config.prevetting import PREVETTING_RULES
from originations.domain.policy.models.policy_rule_runner import (
    PolicyRuleRunner,
)


async def prevetting_endpoint(request: ApplicationRequest):
    policy_rules = PolicyRuleRunner(
        request.application_id, request.applicant_hash, PREVETTING_RULES
    )

    policy_rules.run_policy_rules(application_request=request)

    _, outcome = await asyncio.gather(
        policy_rules.save_policy_outcomes(),
        policy_rules.get_final_policy_outcome(),
    )

    return outcome
