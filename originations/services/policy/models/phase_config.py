from dataclasses import Field, dataclass

from originations.enums.policy import PolicyOutcome, PolicyPhase, ReferralType
from originations.services.policy.models.policy_rule import PolicyRule


@dataclass
class PolicyRuleConfig:
    rule: PolicyRule
    triggered_outcome: PolicyOutcome
    errored_outcome: PolicyOutcome
    referral_types: list[ReferralType] = Field(default_factory=list)


@dataclass
class PolicyPhaseConfig:
    phase: PolicyPhase
    rules: list[PolicyRuleConfig]
