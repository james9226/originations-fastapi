from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, condecimal


class Quote(BaseModel):
    id: UUID
    application_id: UUID
    is_requested: bool
    amount: int
    term: int


class QuoteRisk(BaseModel):
    risk_score: condecimal(max_digits=24, decimal_places=8)
    risk_segment: int


class QuotePricing(BaseModel):
    apr: Optional[condecimal(max_digits=24, decimal_places=8)]
    monthly_payment: Optional[condecimal(max_digits=24, decimal_places=8)]
    total_repayable: Optional[condecimal(max_digits=24, decimal_places=8)]


class QuoteAffordability(BaseModel):
    di: condecimal(max_digits=24, decimal_places=8)
    dti: condecimal(max_digits=24, decimal_places=8)
    min_income_required: condecimal(max_digits=24, decimal_places=8)


class QuoteCalculation(Quote):
    risk: Optional[QuoteRisk]
    pricing: Optional[QuotePricing]
    affordability: Optional[QuoteAffordability]
    failed_policy: list[PolicyRuleComplete] = Field(default_factory=list())
