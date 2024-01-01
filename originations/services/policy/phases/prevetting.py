from originations.enums.policy import PolicyOutcome, PolicyPhase
from originations.services.policy.models.phase_config import (
    PolicyPhaseConfig,
    PolicyRuleConfig,
)
from originations.services.policy.rules.minimum_age_rule import MinimumAgeRule


class UPLPrevettingConfig(PolicyPhaseConfig):
    name: PolicyPhase.PREVETTING

    rules = [
        PolicyRuleConfig(
            rule=MinimumAgeRule,
            triggered_outcome=PolicyOutcome.DECLINED_WITH_REAPPLICATION_ALLOWED,
            errored_outcome=PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
        )
    ]
