import datetime
from typing import Sequence
import uuid
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyOutcome, PolicyRuleResult
from originations.services.firestore.firestore import load_firestore
from originations.services.firestore.io import post_event
from originations.services.logging import log_handler


class PolicyRuleRunner:
    def __init__(
        self, reference_id: uuid.UUID, applicant_hash: str, config: Sequence[PolicyRule]
    ):
        self.config = config
        self.applicant_hash = applicant_hash
        self.reference_id = reference_id

    def run_policy_rules(self, *args, **kwargs):
        self.rule_results = [x.run_rule(**kwargs) for x in self.config]

    async def save_policy_outcomes(self):
        firestore = await load_firestore()
        collection = firestore.collection("policy_outcomes")

        batch = firestore.batch()

        for result in self.rule_results:
            doc_ref = collection.document(str(uuid.uuid4()))
            body = {
                "rule": result.rule_name,
                "result": result.result,
                "outcome": result.outcome,
                "reason": result.reason,
                "event_time": str(datetime.datetime.now()),
                "reference_id": str(self.reference_id),
            }
            batch.set(doc_ref, body)

        await batch.commit()

    async def save_policy_triggers(self):
        await post_event(
            "quotation_triggers_state_store",
            self.applicant_hash,
            {
                "event_time": datetime.datetime.now(),
                "triggered_rules": [
                    x.rule_name
                    for x in self.rule_results
                    if x.result == PolicyRuleResult.TRIGGERED
                ],
            },
        )

    async def get_final_policy_outcome(self):
        priority_order = [
            PolicyOutcome.DECLINED,
            PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
            PolicyOutcome.DECLINED_WITH_REAPPLICATION_ALLOWED,
            PolicyOutcome.REFERRED,
            PolicyOutcome.REFERRED_DUE_TO_TECHNICAL_ERROR,
            PolicyOutcome.PASSED,
        ]
        for outcome in priority_order:
            if any(o.outcome == outcome for o in self.rule_results):
                return outcome
        return PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR
