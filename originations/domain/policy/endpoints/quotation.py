import asyncio
from typing import Optional
from originations.models.application import ApplicationRequest
from originations.domain.policy.phase_config.quotation import QUOTATION_RULES
from originations.domain.policy.models.policy_rule_runner import (
    PolicyRuleRunner,
)


async def quotation_endpoint(request: ApplicationRequest, price: Optional[float]):
    policy_rules = PolicyRuleRunner(
        request.application_id, request.applicant_hash, QUOTATION_RULES
    )

    policy_rules.run_policy_rules(application_request=request, price=price)

    _, _, outcome = await asyncio.gather(
        policy_rules.save_policy_outcomes(),
        policy_rules.save_policy_triggers(),
        policy_rules.get_final_policy_outcome(),
    )

    return outcome
