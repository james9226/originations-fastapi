from originations.services.firestore.firestore import load_firestore
from originations.services.firestore.format import format_dict


async def post_event(collection: str, document_id: str, body: dict) -> None:
    formatted_body = await format_dict(body)
    firestore = await load_firestore()

    collection_ref = firestore.collection(collection)

    await collection_ref.document(document_id).set(formatted_body)
