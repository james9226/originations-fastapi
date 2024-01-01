

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from originations.enums.policy import PolicyPhase
from originations.services.policy.models.phase_config import PolicyRuleConfig


class AbstractPolicyService(ABC):
    def __init__(self, db : AsyncSession, rule_config : PolicyRuleConfig):
        self.db = db 
        self.rule_config = rule_config


    @abstractmethod
    def run_policy_phase(self) -> None:
        raise NotImplementedError()
    

    def run_policy_for_quote
    

class UPLPrevettingPolicyService(AbstractPolicyService):

    def run_policy_phase(self, applicant_id : UUID, customer_id : Optional[UUID]):
        pass 
    

class PolicyServiceFactory:
    def __init__(self, db : AsyncSession):
        self.db = db 

    def yield_policy_service(self, phase : PolicyPhase) -> AbstractPolicyService:
        match phase:
            case PolicyPhase.PREVETTING:
                return UPLPrevettingPolicyService(self.db)
            
    




