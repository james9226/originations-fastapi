import logging
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from originations.services.cloudsql.config import DBSettings

logger = logging.getLogger("loans-event-processor-logger")


def get_async_engine(db_settings: DBSettings) -> AsyncEngine:
    """
    Creates an async SQLAlchemy Engine.
    """
    DATABASE_DRIVER = "postgresql+asyncpg"

    # build the connection string for asyncpg
    DATABASE_URL = URL.create(
        drivername=DATABASE_DRIVER,
        database=db_settings.db_name,
        username=db_settings.db_user,
        password=db_settings.db_password,  # TODO - hide this within secrets manager! Get out of the env!
        host=db_settings.db_host,
        port=db_settings.db_port,
    )

    # create an async engine
    engine = create_async_engine(DATABASE_URL, pool_size=5, max_overflow=15, echo=False)
    logger.warn("Created async connection pool with Cloud SQL")

    return engine
