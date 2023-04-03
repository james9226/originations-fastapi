from datetime import datetime
import uuid
from originations.enums.policy import PolicyRuleResult, PolicyOutcome
import logging
import importlib
from originations.services.firestore.io import post_event


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
        self.logger = logging.getLogger("api-logger")
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

        self.logger.info({"rule": self.rule_name, "result:": result, "reason": reason})
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
