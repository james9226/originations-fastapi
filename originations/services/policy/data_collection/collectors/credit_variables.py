from originations.services.credit_variables.service import CreditVariablesService
from originations.services.policy.data_collection.models.call_result import (
    ServiceCallResult,
    ServiceCall,
)
from originations.services.policy.data_collection.models.input import DataInput


class CreditVariablesInput(DataInput):
    dependencies = []

    async def collect_service_calls(self, variable_id, *args, **kwargs) -> ServiceCall:
        variables_service = CreditVariablesService(self.db)

        try:
            variables = await variables_service.get_credit_variables(variable_id)
            if variables:
                self.service_call = ServiceCall(
                    result=ServiceCallResult.OK, data=variables
                )
            self.service_call = ServiceCall(
                result=ServiceCallResult.FAIL,
                data=None,
                message=f"Unable to find credit variables for application with variable_id {variable_id}!",
            )
        except Exception as e:
            self.service_call = ServiceCall(
                result=ServiceCallResult.FAIL, data=None, message=e
            )
