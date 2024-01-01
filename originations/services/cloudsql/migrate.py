from originations.models import sqlmodels as sq

from originations.services.cloudsql.initialize import get_engine


async def perform_cloudsql_migration():
    engine = get_engine()

    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(sq.SQLModel.metadata.create_all)
