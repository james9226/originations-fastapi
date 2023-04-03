from google.cloud.firestore import AsyncClient
from originations.services.firestore.config import load_credentials


async def load_firestore() -> AsyncClient:
    db = AsyncClient(project="firebase-svelte-381023", credentials=load_credentials())
    return db
