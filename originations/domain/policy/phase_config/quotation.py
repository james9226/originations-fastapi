from typing import Sequence
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyOutcome

from originations.domain.policy.rules.pricing import PricingRule

QUOTATION_RULES: Sequence[PolicyRule] = (
    PricingRule(PolicyOutcome.DECLINED, PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR),
)
