from datetime import datetime
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyRuleResultType
from originations.services.policy.data_collection.collectors.applicant import (
    ApplicantInput,
)


class MinimumAgeRule(PolicyRule):
    name = "Minimum Age Rule"

    def rule(self, applicant_input: ApplicantInput):
        MINIMUM_AGE_THRESHOLD = 18

        if x := self.require(applicant_input):
            return x

        applicant = applicant_input.service_call.data

        age = datetime.today().date() - applicant.date_of_birth

        if age < MINIMUM_AGE_THRESHOLD:
            return self.result(
                result=PolicyRuleResultType.TRIGGERED,
                reason=f"Applicant's age of {age} is less than the threshold of {MINIMUM_AGE_THRESHOLD}",
            )

        return self.result(
            result=PolicyRuleResultType.NOT_TRIGGERED,
            reason=f"Applicant's age of {age} is greater or equal to the threshold of {MINIMUM_AGE_THRESHOLD}",
        )
