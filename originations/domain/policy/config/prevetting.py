from originations.domain.policy.policy_rule import PolicyRuleRunner, PolicyRule
from originations.enums.policy import PolicyOutcome
from originations.domain.policy.rules.age import AgeRule

CONFIG = [
    PolicyRule(
        "age",
        PolicyOutcome.DECLINED,
        PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
    ),
    PolicyRule(
        "minincome",
        PolicyOutcome.DECLINED,
        PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
    ),
    PolicyRule(
        "employment_status",
        PolicyOutcome.DECLINED,
        PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
    ),
]

PREVETTING_CONFIG = [
    PolicyRuleRunner(
        AgeRule, PolicyOutcome.DECLINED, PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR
    )
]
