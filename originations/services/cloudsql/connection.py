import asyncpg
from google.cloud.sql.connector import create_async_connector, IPTypes
from concurrent.futures import ThreadPoolExecutor

from originations.services.cloudsql.config import db_settings

executor = ThreadPoolExecutor()

connection: asyncpg.Connection = None


async def getconn() -> asyncpg.Connection:
    connector = await create_async_connector()
    conn: asyncpg.Connection = await connector.connect_async(
        db_settings.db_connection_name,
        "asyncpg",
        user=db_settings.db_user,
        password=db_settings.db_password,
        db=db_settings.db_name,
        ip_type=IPTypes.PUBLIC,  # IPTypes.PRIVATE for private IP
    )

    return conn
