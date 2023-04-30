from pydantic import BaseModel


class PastTriggers(BaseModel):
    applicant_hash: str
    triggered_rules: list[str]
