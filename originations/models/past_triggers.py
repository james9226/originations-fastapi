from datetime import datetime
from pydantic import BaseModel


class PastTriggers(BaseModel):
    event_time: datetime
    triggers: list[str]
