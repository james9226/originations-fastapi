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


from originations.domain.policy.policy_rule import NewPolicyRule


class AgeRule(NewPolicyRule):
    MIN_AGE = 18

    def __init__(self, request: ApplicationRequest):
        self.request = request
        self.rule_name = "AgeRule"
        self.rule_description = "Check customer is at least 18 years old"

    def run_policy(self) -> None:
        age = (date.today() - self.request.date_of_birth).days / 365.25

        if age < self.MIN_AGE:
            self.result = PolicyRuleResult.TRIGGERED
            self.reason = f"Unnaceptable applicant age of {age}"

        self.result = PolicyRuleResult.NOT_TRIGGERED
        self.reason = f"Acceptable applicant age of {age}"
