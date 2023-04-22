from abc import ABC, abstractmethod
import uuid
from originations.domain.policy.policy_rule import (
    PolicyRule,
    NewPolicyRule,
    PolicyRuleRunner,
)
from originations.enums.policy import PolicyOutcome, PolicyPhase
import asyncio
from originations.models.application import ApplicationRequest
from originations.services.firestore.firestore import load_firestore
import importlib

policy_rule_config = list[PolicyRule]

new_policy_rule_config = list[PolicyRuleRunner]


async def run_policy(
    config: policy_rule_config, reference_id: uuid.UUID, **kwargs
) -> list[dict]:
    policy_rule_outcomes = await asyncio.gather(
        *[x.run_policy_rule(reference_id, **kwargs) for x in config]
    )
    return policy_rule_outcomes


async def save_policy_outcomes(outcomes: list[dict], reference_id: uuid.UUID) -> None:
    firestore = await load_firestore()
    collection = firestore.collection("policy_outcomes")

    batch = firestore.batch()

    for outcome in outcomes:
        doc_ref = collection.document(str(uuid.uuid4()))
        body = {
            "rule": outcome["rule_name"],
            "result": outcome["result"],
            "outcome": outcome["outcome"],
            "reason": outcome["reason"],
            "event_time": outcome["event_time"],
            "reference_id": str(reference_id),
        }
        batch.set(doc_ref, body)

    await batch.commit()


async def run_policy_rules(
    config: policy_rule_config, reference_id: uuid.UUID, **kwargs
) -> PolicyOutcome:
    policy_rule_outcomes = await run_policy(config, reference_id, **kwargs)

    # Save the outcomes to the database in a single batch operation
    await save_policy_outcomes(policy_rule_outcomes, reference_id)

    # Define the order of priority for PolicyOutcome values
    priority_order = [
        PolicyOutcome.DECLINED,
        PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
        PolicyOutcome.DECLINED_WITH_REAPPLICATION_ALLOWED,
        PolicyOutcome.REFERRED,
        PolicyOutcome.REFERRED_DUE_TO_TECHNICAL_ERROR,
        PolicyOutcome.PASSED,
    ]

    # Iterate through the priority_order list and return the first matching outcome
    for outcome in priority_order:
        if any(o["outcome"] == outcome for o in policy_rule_outcomes):
            return outcome
    # Safety catch-all (this should never happen)
    return PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR


class PolicyController:
    def __init__(
        self, config: new_policy_rule_config, reference_id: uuid.UUID, **kwargs
    ):
        self.reference_id = reference_id
        self.policy: list[PolicyRuleRunner] = asyncio.gather(
            *[x(**kwargs) for x in config]
        )

    async def run_phase_policy(self):
        self.policy_results: list[PolicyRuleRunner] = await asyncio.gather(
            *[x.run_policy_rule() for x in self.policy]
        )

    async def get_phase_outcome(self) -> PolicyOutcome:
        priority_order = [
            PolicyOutcome.DECLINED,
            PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
            PolicyOutcome.DECLINED_WITH_REAPPLICATION_ALLOWED,
            PolicyOutcome.REFERRED,
            PolicyOutcome.REFERRED_DUE_TO_TECHNICAL_ERROR,
            PolicyOutcome.PASSED,
        ]

        # Iterate through the priority_order list and return the first matching outcome
        for outcome in priority_order:
            if any(o.get_result() == outcome for o in self.policy_results):
                return outcome
        # Safety catch-all (this should never happen)
        return PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR

    async def save_policy_outcomes(self) -> None:
        firestore = await load_firestore()
        collection = firestore.collection("policy_outcomes")

        batch = firestore.batch()

        for outcome in self.policy_results:
            doc_ref = collection.document(str(uuid.uuid4()))
            body = {
                "rule": outcome.get_name(),
                "result": outcome.get_result(),
                "outcome": outcome.get_outcome(),
                "reason": outcome.get_reason(),
                "event_time": outcome.get_event_time(),
                "reference_id": self.reference_id,
            }
            batch.set(doc_ref, body)

        await batch.commit()


async def run_new_policy(
    config: new_policy_rule_config, reference_id: uuid.UUID, **kwargs
) -> PolicyOutcome:
    controller = PolicyController(config, reference_id, **kwargs)

    await controller.run_phase_policy()

    await controller.save_policy_outcomes()

    return await controller.get_phase_outcome()
