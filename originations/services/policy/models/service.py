from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from originations.models.credit_variables import CreditVariables
from originations.models.quotes import QuoteCalculation
from originations.models.sqlmodels import Applicant
from originations.services.policy.models.policy_rule import (
    PolicyPhaseConfig,
)
from originations.services.pubsub.service import PubSubPublisherService
from originations.services.triggers.service import TriggersService


class PolicyRuleService:
    def __init__(
        self,
        db: AsyncSession,
        pub_sub_publisher: PubSubPublisherService,
    ):
        self.db = db
        self.pub_sub_pulisher = pub_sub_publisher

    async def run_policy_phase(
        self,
        quotes: list[QuoteCalculation],
        applicant: Applicant,
        credit_variables: Optional[CreditVariables],
        policy_config : PolicyPhaseConfig
    ):
        pass

    async def run_policy_for_quote(
        self,
        quote : QuoteCalculation,
        applicant: Applicant,
        credit_variables: Optional[CreditVariables],
        policy_config : PolicyPhaseConfig
    )
