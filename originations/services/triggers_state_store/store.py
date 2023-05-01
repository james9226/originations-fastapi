import asyncio
from datetime import datetime
from originations.enums.policy import PolicyPhase
from originations.services.firestore.firestore import load_firestore
from originations.models.past_triggers import PastTriggers


async def save_policy_triggers(hash: str, phase: str, triggers: list[str]):
    firestore = await load_firestore()

    reference = (
        firestore.collection("triggers_store")
        .document(hash)
        .collection(phase)
        .document("latest")
    )

    await reference.set({"event_time": datetime.now(), "triggers": triggers})


async def get_phase_policy_triggers(hash: str, phase: PolicyPhase):
    firestore = await load_firestore()
    reference = (
        firestore.collection("triggers_store")
        .document(hash)
        .collection("quotation")
        .document("latest")
    )

    return await reference.get().to_dict()


async def get_phase_policy_triggers(hash: str, phase: PolicyPhase):
    firestore = await load_firestore()
    reference = (
        firestore.collection("triggers_store")
        .document(hash)
        .collection(phase)
        .document("latest")
    )

    data = await reference.get()

    data_dict = data.to_dict()

    if data_dict is not None:
        return PastTriggers(**data_dict)

    return None


async def get_policy_triggers(hash: str):
    coros = [get_phase_policy_triggers(hash, phase) for phase in PolicyPhase]

    res = await asyncio.gather(*coros)

    return [x for x in res if x is not None]
