from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional
from originations.domain.policy.models.policy_rule_completion import PolicyRuleComplete
from originations.enums.policy import (
    PolicyOutcome,
    PolicyRuleResultType,
    ReferralType,
)
from originations.models.credit_variables import CreditVariables

from originations.models.quotes import QuoteCalculation
from originations.models.sqlmodels import Applicant

import inspect
from originations.services.policy.data_collection.models.call_result import (
    ServiceCallResult,
)

from originations.services.policy.data_collection.models.input import (
    DataInput,
    DataInputType,
)


@dataclass
class PolicyRuleResult:
    rule: str
    result: PolicyRuleResultType
    reason: str


class PolicyRule(ABC):
    name: str = ""

    def get_dependancies(self) -> Dict[str, DataInputType]:
        return inspect.get_annotations(self.rule)

    def run_rule(self, data_inputs: Dict[DataInputType, DataInput]):
        rule_inputs = {}

        for name, input in self.get_dependancies().items():
            input = data_inputs.get(input)

            if not input:
                # Critical Error

                raise ValueError("This should never happen!")

            rule_inputs[name] = input

        return self.rule(**rule_inputs)

    def require(
        self, input: DataInput, null_data_dissallowed: bool = True
    ) -> Optional[PolicyRuleResult]:
        if input.service_call.result == ServiceCallResult.FAIL:
            return PolicyRuleResult(
                rule=self.name,
                result=PolicyRuleResultType.ERRORED,
                reason=f"Collector of type {type(input).__name__} failed with message {input.service_call.message}",
            )

        if null_data_dissallowed and input.service_call.data is None:
            return PolicyRuleResult(
                rule=self.name,
                result=PolicyRuleResultType.ERRORED,
                reason=f"Collector of type {type(input).__name__} succeeded however contained no data, which is required",
            )
        return None

    @abstractmethod
    def rule(self) -> PolicyRuleResult:
        raise NotImplementedError()

    def result(
        self, result_type: PolicyRuleResultType, reason: str
    ) -> PolicyRuleResult:
        return PolicyRuleResult(rule=self.name, result=result_type, reason=reason)
