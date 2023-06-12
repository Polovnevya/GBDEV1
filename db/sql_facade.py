from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, engine
import asyncio
from models import Base, Candidate, Employer, Audience, Vacancy, Feedback, Post, Channel
from fixtures import fixtures
from settings import connection_string


class SqlManage:
    def __init__(self):
        self.async_engine = None
        self.async_session = None

    async def create_async_engine(self) -> engine.AsyncEngine:
        self.async_engine = create_async_engine(
            connection_string,
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


class SqlHelper:

    def __init__(self):
        self.sm = SqlManage()

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


async def main() -> None:
    sh = SqlHelper()
    await sh.insert_objects(fixtures)


asyncio.run(main())
