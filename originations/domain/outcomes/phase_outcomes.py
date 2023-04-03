from originations.enums.policy import PolicyOutcome
import logging


def phase_outcome_decider(policy_outcome, phase):
    declined_outcomes = [
        PolicyOutcome.DECLINED,
        PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
        PolicyOutcome.DECLINED_WITH_REAPPLICATION_ALLOWED,
    ]
    logger = logging.getLogger("api-logger")

    if policy_outcome in declined_outcomes:
        logger.info(
            f"Evaluated a {policy_outcome} outcome at phase {phase} - stopping application"
        )
        return True
    logger.info(f"Evaluated a pass outcome at phase {phase}")
    return False
