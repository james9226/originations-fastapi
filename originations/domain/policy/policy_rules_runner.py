import uuid
from originations.domain.policy.policy_rule import PolicyRule
from originations.enums.policy import PolicyOutcome
import asyncio

from originations.services.firestore.firestore import load_firestore

policy_rule_config = list[PolicyRule]


async def run_policy(config: policy_rule_config, reference_id, **kwargs):
    policy_rule_outcomes = await asyncio.gather(
        *[x.run_policy_rule(reference_id, **kwargs) for x in config]
    )
    return policy_rule_outcomes


async def save_policy_outcomes(outcomes: list, reference_id):
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


async def run_policy_rules(config: policy_rule_config, reference_id, **kwargs):
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
