from originations.domain.policy.policy_rule import PolicyRule
from originations.enums.policy import PolicyOutcome

PREVETTING_CONFIG = [
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
