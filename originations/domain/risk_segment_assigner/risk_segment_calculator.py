from originations.domain.risk_segment_assigner.config import RISK_SEGMENT_CUTOFFS
from originations.services.logging import log_handler


async def risk_segment_calculator(risk_score: float) -> int:
    segment = max(
        (k for k, v in RISK_SEGMENT_CUTOFFS.items() if v > risk_score), default=1
    )
    log_handler.info(f"Assigned risk segment of {segment}")
    return segment
