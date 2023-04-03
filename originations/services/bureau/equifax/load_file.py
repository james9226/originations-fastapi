from originations.middleware.context import get_request_id
from originations.models.application import ApplicationRequest
from datetime import datetime, timedelta
from originations.services.bureau.equifax.mock_endpoint import create_mock_bureau_file
from originations.services.firestore.firestore import load_firestore
import asyncio
import logging

logger = logging.getLogger("api-logger")


async def load_existing_credit_file(applicant_hash: str) -> list:
    firestore = await load_firestore()

    collection = (
        firestore.collection("credit_files")
        .document(applicant_hash)
        .collection("equifax")
    )
    query = collection.where("expirey_timestamp", ">=", str(datetime.now()))

    docs = await query.get()

    return docs


async def save_new_credit_file(applicant_hash: str, credit_file) -> None:
    firestore = await load_firestore()

    collection = (
        firestore.collection("credit_files")
        .document(applicant_hash)
        .collection("equifax")
    )

    body = {
        "expirey_timestamp": str(datetime.now() + timedelta(days=30)),
        "created_timestamp": str(datetime.now()),
        "credit_file": credit_file,
    }

    await collection.document().set(body)


async def mock_equifax_request(request: ApplicationRequest):
    # if no valid cached file, external request to get new one

    res = await load_existing_credit_file(request.applicant_hash)

    if len(res) == 1:
        logger.info(f"Found existing credit file for request {get_request_id()}")
        return res[0].to_dict()["credit_file"]
    if len(res) > 1:
        logger.error("Found duplicate files")
        raise ValueError("Duplicate Valid Credit Files For Applicant!")

    logger.info(f"Creting new credit file for request {get_request_id()}")

    # Fake External Request
    credit_file = await create_mock_bureau_file()

    await save_new_credit_file(request.applicant_hash, credit_file)

    return credit_file
