from typing import Tuple
from originations.models.application import ApplicationRequest
from originations.enums.policy import PolicyRuleResult


async def rule(request: ApplicationRequest) -> Tuple[PolicyRuleResult, str]:
    MIN_INCOME = 12000

    if request.gross_annual_income < MIN_INCOME:
        return (
            PolicyRuleResult.TRIGGERED,
            f"Unnaceptable income of {request.gross_annual_income}",
        )
    return (
        PolicyRuleResult.NOT_TRIGGERED,
        f"Acceptable income of {request.gross_annual_income}",
    )
