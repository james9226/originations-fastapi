from typing import Tuple
from originations.models.application import ApplicationRequest
from originations.enums.policy import PolicyRuleResult
from datetime import date


async def rule(request: ApplicationRequest) -> Tuple[PolicyRuleResult, str]:
    MIN_AGE = 18

    age = (date.today() - request.date_of_birth).days / 365.25

    if age < MIN_AGE:
        return PolicyRuleResult.TRIGGERED, f"Unnaceptable applicant age of {age}"
    return PolicyRuleResult.NOT_TRIGGERED, f"Acceptable applicant age of {age}"
