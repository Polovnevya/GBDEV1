from typing import List
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, engine
from .models import Base, Candidate, Employer, Audience, Vacancy, Feedback, Post, Channel, channel_to_audience
from config.config import Config
from .mixins.candidate import DAOCandidateMixin
from .mixins.vacancy import DAOVacancyMixin
from .mixins.feedback import DAOFeedbackMixin
from .mixins.emloyer import DAOEmployerData
from .mixins.channel import DAOChannelMixin


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


class DAO(DAOCandidateMixin, DAOFeedbackMixin, DAOVacancyMixin, DAOEmployerData, DAOChannelMixin):
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
                        kwargs.pop('_sa_instance_state')
                        stmt = select(key).filter_by(**kwargs)
                        result = await session.scalar(stmt)

                        if not result:
                            session.add(key(**kwargs))
                            session.commit()

                channel1 = await session.scalar(select(Channel).filter_by(id=1))
                channel2 = await session.scalar(select(Channel).filter_by(id=2))
                audience1 = await session.scalar(select(Audience).filter_by(id=1))
                audience2 = await session.scalar(select(Audience).filter_by(id=2))
                if audience1 not in channel1.audience and audience2 not in channel1.audience:
                    channel1.audience.append(audience1)
                    channel1.audience.append(audience2)
                if audience1 not in channel2.audience:
                    channel2.audience.append(audience1)
                session.commit()

