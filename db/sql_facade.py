from typing import Union

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, engine
from .models import Base, Candidate, Employer, Audience, Vacancy, Feedback, Post, Channel
from .fixtures import fixtures
from config.config import Config


class SqlManage:
    def __init__(self, config: Config):
        self.async_engine = None
        self.async_session = None
        self.connection_string = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"

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


# TODO Антон - переписать скрытую зависимость  self.sm: SqlManage, на DI
class SqlHelper:
    def __init__(self, config: Config):
        self.sm: SqlManage = SqlManage(config)

    # TODO Антон - переписать, разбить метод на отедбные - 1) проверка на наличие и создание таблиц 2) И метод загрузки фикстур
    async def insert_objects(self, datas: dict) -> None:
        await self.sm.create_async_engine()
        await self.sm.drop_all_tables()
        await self.sm.create_all_tables()
        await self.sm.create_async_session()
        async with self.sm.async_session() as session:
            async with session.begin():
                candidates = [Candidate(**candidate) for candidate in fixtures.get("candidate")]
                employers = [Employer(**employer) for employer in fixtures.get("employer")]
                audiences = [Audience(**audience) for audience in fixtures.get("audience")]
                vacancies = [Vacancy(**vacancy) for vacancy in fixtures.get("vacancy")]
                feedbacks = [Feedback(**feedback) for feedback in fixtures.get("feedback")]
                channels = [Channel(**channel) for channel in fixtures.get("channel")]
                posts = [Post(**post) for post in fixtures.get("post")]
                session.add_all(
                    [
                        *candidates,
                        *employers,
                        *audiences,
                        *vacancies,
                        *feedbacks,
                        *channels,
                        *posts,
                    ]
                )

    #TODO запилить реализацию
    async def get_candidate_by_id(self, candidate_tg_id: int) -> Union[dict, bool]:
        """
        ищет по tg_id кандидата, если он не удален
        :param candidate_tg_id:
        :return: возвращает данные кандидата в виде словаря если он имеется в таблице и False если такого кандидата в базе нет
        """
        return {'first_name': 'Юрий',
            'middle_name': 'Андреевич',
            'last_name': 'Половнев',
            'gender': 'male',
            'age': 'senior',      # тут должны быть значения энамов, а не ключи
            'education': 'higher',
            'phone': '+79134903369',
            'tg_id': 618432846}

    #TODO запилить реализацию
    async def insert_or_update_candidate(self, candidate_data: dict) -> None:
        """
        Принимает словарь с данными кандидата
            {'first_name': 'ф',
            'middle_name': 'ы',
            'last_name': 'в',
            'gender': 'female',
            'age': 'senior',
            'education': 'higher',
            'phone': '+79134903369',
            'tg_id': 618432846}

        производит добавление кандидата если его нет
        и
        обновляет данные кандидата если он уже есть в базе
        можно разбить на 2 метода добавление и обновление, а этот использовать как фасад

        :param candidate_data:
        :return:
        """
        pass
    #TODO запилить реализацию
    async def get_active_employers_by_id(self) -> list[int]:
        """
        1) не удален
        :param employer_tg_id:
        :return:
        """
        pass

# async def main() -> None:
#     sh = SqlHelper()
#     await sh.insert_objects(fixtures)
