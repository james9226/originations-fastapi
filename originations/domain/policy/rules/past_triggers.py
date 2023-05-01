from datetime import datetime, timezone
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyRuleResult
from originations.models.past_triggers import PastTriggers


class PastTriggersRule(PolicyRule):
    rule_name = "PastTriggersRule"

    def rule(
        self,
        past_triggers: list[PastTriggers],
        *args,
        **kwargs,
    ):
        blocked_rules = [
            "PricingRule",
            "MissedPaymentsLast12M",
        ]

        recent_triggers: list[list[str]] = [
            x.triggers
            for x in past_triggers
            if (datetime.now((timezone.utc)) - x.event_time).days < 180
        ]
        flattened_triggers: list[str] = [
            trigger for sublist in recent_triggers for trigger in sublist
        ]

        valid_triggers: list[str] = [
            trigger for trigger in flattened_triggers if trigger in blocked_rules
        ]

        if len(valid_triggers) > 0:
            return self.result(
                PolicyRuleResult.TRIGGERED,
                f"Applicant has been recently declined for {str(valid_triggers)}",
            )

        return self.result(
            PolicyRuleResult.NOT_TRIGGERED,
            f"Applicant has not been recently declined for any blocking rule!",
        )
