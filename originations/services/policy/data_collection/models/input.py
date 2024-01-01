from abc import ABC
from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

from originations.services.policy.data_collection.models.call_result import (
    ServiceCall,
    ServiceCallResult,
)


class DataInput(ABC):
    dependencies: list["DataInput"] = []

    def __init__(self, db: AsyncSession):
        self.db = db

    async def collect_service_calls(self, *args, **kwargs):
        self.service_call = ServiceCall(
            result=ServiceCallResult.FAIL,
            data=None,
            message=f"This Data Collector has not been Implemented!",
        )
        pass


DataInputType = TypeVar("DataInputType", bound=DataInput)
