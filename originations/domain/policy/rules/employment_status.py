from typing import Tuple
from originations.models.application import ApplicationRequest
from originations.enums.policy import PolicyRuleResult
from originations.enums.enums import EmploymentStatus


async def rule(request: ApplicationRequest) -> Tuple[PolicyRuleResult, str]:
    acceptable_employment_statuses = [
        EmploymentStatus.FULL_TIME,
        EmploymentStatus.PART_TIME,
        EmploymentStatus.RETIRED,
        EmploymentStatus.SELF_EMPLOYED,
    ]

    employment_status = request.employment_status

    if employment_status in acceptable_employment_statuses:
        return (
            PolicyRuleResult.NOT_TRIGGERED,
            f"Acceptable employment status of {employment_status}",
        )
    return (
        PolicyRuleResult.TRIGGERED,
        f"Unnaceptable employment status of {employment_status}",
    )
