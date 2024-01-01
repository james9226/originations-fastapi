from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from originations.enums.policy import PolicyOutcome
from originations.models.sqlmodels import ApplicationDecision
from originations.services.decision.service import DecisionService

from originations.services.logging.log_handler import get_logger


class BaseLendotopiaException(Exception, ABC):
    def __init__(
        self,
        message: str,
        db: AsyncSession,
        application_id: UUID,
        applicant_id: Optional[UUID],
        credit_profile_id: Optional[UUID],
        decision: PolicyOutcome,
        reason: str,
    ):
        super().__init__(message)
        self.logger = get_logger()
        self.message = message
        self.decision_service = DecisionService(db)
        self.decision = self.decision_service.create_decision(
            application_id=application_id,
            decision=decision,
            reason=reason,
            applicant_id=applicant_id,
            credit_profile_id=credit_profile_id,
            quotes=[],
        )

    async def raise_with_db_save(self):
        # Use the exception_type in the logging message
        log_message = f"{self.exception_type}: {self.message}"
        self.log(log_message)
        await self.decision_service.save_decision(self.decision)
        raise self

    @abstractmethod
    def log(self, log_message) -> None:
        pass

    @property
    @abstractmethod
    def exception_type(self) -> str:
        """This property should return a string representing the type of the exception."""
        pass


class UnauthorizedError(BaseLendotopiaException):
    @property
    def exception_type(self) -> str:
        return "UnauthorizedError"

    def log(self, log_message) -> None:
        self.logger.error(log_message)


class ServiceCallFailure(BaseLendotopiaException):
    @property
    def exception_type(self) -> str:
        return "ServiceCallFailure"

    def log(self, log_message) -> None:
        self.logger.error(log_message)


class ServiceCallTimeout(BaseLendotopiaException):
    @property
    def exception_type(self) -> str:
        return "ServiceCallTimeout"

    def log(self, log_message) -> None:
        self.logger.error(log_message)


class UnexpectedError(BaseLendotopiaException):
    @property
    def exception_type(self) -> str:
        return "Unexpected"

    def log(self, log_message) -> None:
        self.logger.error(log_message)


class DeclinedException(BaseLendotopiaException):
    @property
    def exception_type(self) -> str:
        return "Declined"

    def log(self, log_message) -> None:
        self.logger.info(log_message)
