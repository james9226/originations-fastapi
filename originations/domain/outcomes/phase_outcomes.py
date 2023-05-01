from datetime import datetime
from originations.enums.policy import PolicyOutcome
from originations.services.firestore.io import post_event
from originations.services.logging import log_handler


async def phase_outcome_decider(application_id, policy_outcome, phase):
    declined_outcomes = [
        PolicyOutcome.DECLINED,
        PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
        PolicyOutcome.DECLINED_WITH_REAPPLICATION_ALLOWED,
    ]

    await post_event(
        f"{phase}_outcomes",
        str(application_id),
        {"outcome": policy_outcome, "event_time": datetime.now()},
    )

    if policy_outcome in declined_outcomes:
        log_handler.info(
            f"Evaluated a {policy_outcome} outcome at phase {phase} - stopping application"
        )
        return True
    log_handler.info(f"Evaluated a pass outcome at phase {phase}")
    return False
