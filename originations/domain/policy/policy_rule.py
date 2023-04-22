from datetime import datetime
import uuid
from originations.enums.policy import PolicyRuleResult, PolicyOutcome
import importlib
from abc import ABC, abstractmethod
from originations.services.firestore.io import post_event
from originations.models.application import ApplicationRequest
from originations.models.credit_variables import CreditVariables
from originations.models.submission_request import SubmissionRequest
from originations.services.logging import log_handler


class PolicyRule:
    def __init__(
        self,
        rule_name,
        triggered_outcome: PolicyOutcome,
        errored_outcome: PolicyOutcome,
    ):
        self.rule_name = rule_name
        self.triggered_outcome = triggered_outcome
        self.errored_outcome = errored_outcome
        self.module = importlib.import_module(
            f"originations.domain.policy.rules.{rule_name}"
        )

    async def run_policy_rule(self, reference_id, **kwargs) -> dict:
        try:
            result, reason = await self.module.rule(**kwargs)
        except:
            result, reason = (
                PolicyRuleResult.ERRORED,
                f"Unhandled error trying to run policy rule {self.rule_name}",
            )

        log_handler.info(f"rule={self.rule_name}, result={result}, reason={reason}")
        if result == PolicyRuleResult.TRIGGERED:
            outcome = self.triggered_outcome
        elif result == PolicyRuleResult.ERRORED:
            outcome = self.errored_outcome
        elif result == PolicyRuleResult.NOT_TRIGGERED:
            outcome = PolicyOutcome.PASSED
        else:
            # Safety catch-all in case something weird happens
            outcome = PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR

        outcome_dict = {
            "rule_name": self.rule_name,
            "outcome": outcome,
            "result": result,
            "reason": reason,
            "reference_id": str(reference_id),
            "event_time": str(datetime.now()),
        }

        return outcome_dict


class NewPolicyRule(ABC):
    def __init__(self, **kwargs):
        self.result = None
        self.reason = None
        self.rule_name = None

    @abstractmethod
    async def run_policy(self):
        return self


class PolicyRuleRunner:
    def __init__(
        self,
        policy: NewPolicyRule,
        triggered_outcome: PolicyOutcome,
        errored_outcome: PolicyOutcome,
        **kwargs,
    ):
        self.policy_rule: NewPolicyRule = policy(**kwargs)
        self.triggered_outcome = triggered_outcome
        self.errored_outcome = errored_outcome

    async def run_policy_rule(self):
        self.policy_rule.run_policy()
        self.event_time = datetime.now()
        return self

    def get_outcome(self) -> PolicyOutcome:
        result = self.policy_rule.result

        if result == PolicyRuleResult.TRIGGERED:
            outcome = self.triggered_outcome
        elif result == PolicyRuleResult.ERRORED:
            outcome = self.errored_outcome
        elif result == PolicyRuleResult.NOT_TRIGGERED:
            outcome = PolicyOutcome.PASSED
        else:
            # Safety catch-all in case something weird happens
            outcome = PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR

        return outcome

    def get_reason(self) -> str:
        return self.policy_rule.result

    def get_name(self) -> str:
        return self.policy_rule.rule_name

    def get_result(self) -> PolicyRuleResult:
        return self.policy_rule.result

    def get_event_time(self) -> datetime:
        return self.event_time
