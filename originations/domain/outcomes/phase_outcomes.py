from originations.enums.policy import PolicyOutcome
from originations.services.logging import log_handler


def phase_outcome_decider(policy_outcome, phase):
    declined_outcomes = [
        PolicyOutcome.DECLINED,
        PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
        PolicyOutcome.DECLINED_WITH_REAPPLICATION_ALLOWED,
    ]

    if policy_outcome in declined_outcomes:
        log_handler.info(
            f"Evaluated a {policy_outcome} outcome at phase {phase} - stopping application"
        )
        return True
    log_handler.info(f"Evaluated a pass outcome at phase {phase}")
    return False
