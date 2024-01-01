from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession
from originations.enums.policy import PolicyPhase
from originations.models.quotes import QuoteCalculated
from originations.models.sqlmodels import Applicant, CreditProfile
from originations.services.policy_legacy.phase_config.quotation import QUOTATION_RULES

from originations.services.policy_legacy.service import PolicyService
from originations.services.pubsub.service import PubSubPublisherService
from originations.services.triggers.service import TriggersService


class AbstractPolicyProcessor(ABC):
    def __init__(
        self,
        db: AsyncSession,
        triggers_service: TriggersService,
        pubsub: PubSubPublisherService,
    ):
        self.db = db
        self.triggers_service = triggers_service
        self.pubsub = pubsub


class MultiQuotePolicyProcessor(AbstractPolicyProcessor):
    async def run_multiquote_policy(
        self,
        quotes: list[QuoteCalculated],
        applicant: Applicant,
        credit_profile: CreditProfile,
    ):
        policy_results = []

        for quote in quotes:
            policy_results: PolicyService = PolicyService(
                self.db,
                self.pubsub,
                quote.id,
                self.triggers_service,
                phase=PolicyPhase.QUOTATION,
                rules=QUOTATION_RULES,
            ).run_policy_rules()
