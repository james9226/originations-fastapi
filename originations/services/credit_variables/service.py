from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from originations.models.sqlmodels import CreditVariables
from originations.services.credit_variables.domain.variable_calculator import (
    calculate_credit_variables,
)


class CreditVariablesService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_credit_variables_to_db(
        self, credit_variables: CreditVariables
    ) -> None:
        try:
            async with self.db.begin():
                self.db.add(credit_variables)

                self.db.commit()

        except:
            raise IOError("Unhandled exception occurred saving variables to DB")

    async def get_credit_variables(
        self, variable_id: UUID
    ) -> Optional[CreditVariables]:
        query = select(CreditVariables).where(CreditVariables.id == variable_id)

        return await self.db.exec(query).one_or_none()

    def calculate_credit_variables(
        self, application_id, credit_file
    ) -> CreditVariables:
        return calculate_credit_variables(credit_file, application_id)
