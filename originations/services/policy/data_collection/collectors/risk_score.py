from originations.services.policy.data_collection.collectors.credit_variables import (
    CreditVariablesInput,
)
from originations.services.policy.data_collection.models.call_result import (
    ServiceCall,
    ServiceCallResult,
)
from originations.services.policy.data_collection.models.input import DataInput


class RiskScoreInput(DataInput):
    dependencies = [CreditVariablesInput]

    async def collect_service_calls(
        self, data_inputs: list[DataInput], *args, **kwargs
    ):
        credit_variables = next(
            (x for x in data_inputs if isinstance(data_inputs, CreditVariablesInput)),
            None,
        )

        self.service_call = ServiceCall(result=ServiceCallResult.OK, data=0.02)
