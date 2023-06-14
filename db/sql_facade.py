from typing import Union
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, engine
from .models import Base, Candidate, Employer, Audience, Vacancy, Feedback, Post, Channel
from config.config import Config
from .types import CandidateData


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


class SqlHelper:
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

    # TODO запилить реализацию
    async def get_candidate_by_id(self, candidate_tg_id: int) -> Union[dict, bool]:
        """
        ищет по tg_id кандидата, если он не удален
        :param candidate_tg_id:
        :return: возвращает данные кандидата в виде словаря если он имеется в таблице
                и False если такого кандидата в базе нет
        """
        return {'first_name': 'Юрий',
                'middle_name': 'Андреевич',
                'last_name': 'Половнев',
                'gender': 'male',
                'age': 'senior',  # тут должны быть значения энамов, а не ключи
                'education': 'higher',
                'phone': '+79134903369',
                'tg_id': 618432846}

    # TODO запилить реализацию
    async def insert_or_update_candidate(self, candidate_data: CandidateData) -> None:
        """
        Принимает dataclass с данными кандидата

        производит добавление кандидата если его нет
        и
        обновляет данные кандидата если он уже есть в базе
        можно разбить на 2 метода добавление и обновление, а этот использовать как фасад

        :param candidate_data:
        :return:
        """

        await self.sql_manager.create_async_session()
        async with self.sql_manager.async_session() as session:
            async with session.begin():
                result = await session.execute(select(Candidate).filter_by(tg_id=candidate_data.tg_id))
                candidate = result.one_or_none()
                if not candidate:
                    session.add(Candidate(**candidate_data.__dict__))
                else:
                    candidate.first_name = candidate_data.first_name
                    candidate.middle_name = candidate_data.middle_name
                    candidate.education = candidate_data.education
                    candidate.age = candidate_data.age
                    candidate.phone = candidate_data.phone
                    candidate.gender = candidate_data.gender

    # TODO запилить реализацию
    async def get_active_employers_by_id(self, employer_tg_id: int) -> list[int]:
        """
        1) не удален
        :param employer_tg_id:
        :return:
        """
        pass

# async def main() -> None:
#     sh = SqlHelper()
#     await sh.insert_objects(fixtures)
