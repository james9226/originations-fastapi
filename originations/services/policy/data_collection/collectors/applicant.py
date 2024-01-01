from uuid import UUID
from originations.services.applicant.service import ApplicantService
from originations.services.credit_variables.service import CreditVariablesService
from originations.services.policy.data_collection.models.call_result import (
    ServiceCallResult,
    ServiceCall,
)
from originations.services.policy.data_collection.models.input import DataInput


class ApplicantInput(DataInput):
    dependencies = []

    async def collect_service_calls(self, applicant_id: UUID, *args, **kwargs) -> None:
        applicant_service = ApplicantService(self.db)

        try:
            applicant = await applicant_service.get_applicant_by_id(applicant_id)
            if applicant:
                self.service_call = ServiceCall(
                    result=ServiceCallResult.OK, data=applicant
                )
            self.service_call = ServiceCall(
                result=ServiceCallResult.FAIL,
                data=None,
                message=f"Unable to find applicant for application with applicant_id {applicant_id}!",
            )
        except Exception as e:
            self.service_call = ServiceCall(
                result=ServiceCallResult.FAIL, data=None, message=e
            )
