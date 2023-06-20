from typing import Union, List
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, engine
from .models import Base, Candidate, Employer, Audience, Vacancy, Feedback, Post, Channel
from config.config import Config
from .mixins.candidate import DAOCandidateMixin


class SqlManager:
    def __init__(self, config: Config):
        self.async_engine = None
        self.async_session = None
        self.async_connection = None
        self.connection_string = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}" \
                                 f"@{config.db.db_host}/{config.db.database}"

    async def create_async_engine(self) -> engine.AsyncEngine:
        self.async_engine = create_async_engine(
            self.connection_string,
            echo=True
        )
        return self.async_engine

    async def drop_all_tables(self) -> None:
        if not self.async_engine:
            raise ValueError("engin not created")
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def create_all_tables(self) -> None:
        if not self.async_engine:
            raise ValueError("engin not created")
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create_async_session(self) -> None:
        if not self.async_engine:
            raise ValueError("engin not created")
        self.async_session = async_sessionmaker(self.async_engine, expire_on_commit=False)

    async def create_async_connection(self) -> None:
        self.async_connection = self.async_engine.connect()


class SqlHelper(DAOCandidateMixin):
    def __init__(self, sql_manager: SqlManager):
        self.sql_manager = sql_manager

    async def delete_db_tables(self, is_delete: bool = False) -> None:
        await self.sql_manager.create_async_engine()
        if is_delete:
            await self.sql_manager.drop_all_tables()

    async def create_db_tables(self) -> None:
        await self.sql_manager.create_async_engine()
        async with self.sql_manager.async_engine.connect() as conn:
            db_table_names = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names()
            )

        metadata_table_names = [table_name for table_name in Base.metadata.tables.keys()]

        metadata_table_names.sort()
        db_table_names.sort()

        if not db_table_names == metadata_table_names:
            await self.sql_manager.create_all_tables()

    async def load_fixtures(self, fixtures: dict) -> None:
        objects = {}
        await self.sql_manager.create_async_session()
        async with self.sql_manager.async_session() as session:
            async with session.begin():
                objects[Candidate] = [Candidate(**candidate) for candidate in fixtures.get("candidate")]
                objects[Employer] = [Employer(**employer) for employer in fixtures.get("employer")]
                objects[Audience] = [Audience(**audience) for audience in fixtures.get("audience")]
                objects[Vacancy] = [Vacancy(**vacancy) for vacancy in fixtures.get("vacancy")]
                objects[Feedback] = [Feedback(**feedback) for feedback in fixtures.get("feedback")]
                objects[Channel] = [Channel(**channel) for channel in fixtures.get("channel")]
                objects[Post] = [Post(**post) for post in fixtures.get("post")]

                for key, items in objects.items():
                    for item in items:
                        kwargs = item.__dict__
                        del kwargs['_sa_instance_state']
                        result = await session.execute(select(key).filter_by(**kwargs))
                        if not result:
                            session.add(item)
