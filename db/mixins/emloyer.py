from typing import Union
from sqlalchemy import select
from ..models import Employer, Vacancy, Post, Feedback
from ..types import DAOEmployerData, Reporting


class DAOEmployerMixin:
    sql_manager = None

    async def get_active_employers_by_id(self, employer_tg_id: int) -> Union[DAOEmployerData, None]:
        """
        1) не удален
        :param employer_tg_id:
        :return:
        """
        await self.sql_manager.create_async_session()
        async with self.sql_manager.async_session() as session:
            async with session.begin():
                stmt = select(Employer).where(Employer.tg_id == employer_tg_id).where(
                    Employer.deleted_at is not None)
                result = await session.scalars(stmt)
                tmp = result.first()
                if tmp:
                    employer = tmp
                    return DAOEmployerData(
                        company_name=employer.company_name,
                        email=employer.email,
                        phone=employer.phone,
                        tg_id=employer.tg_id,
                    )

    async def get_reporting(self, employer_id: int) -> list[Reporting]:
        """
        возвращает список кортежей.
        в каждом кортеже содержиться информация относительно одной вакансии, а именно:
        - id вакансии;
        - наименование вакансии;
        - количество опубликованных постов с вакансией;
        - количество откликов на вакансию.
        Вакансии которые были удалены, и отклики по ним, не учитываются.

        """
        reports = []

        await self.sql_manager.create_async_session()
        async with self.sql_manager.async_session() as session:
            async with session.begin():
                vacancy_stmt = select(Vacancy).where(Vacancy.employer_id == employer_id).where(
                    Vacancy.deleted_at is not None)
                vacancies = await session.scalars(vacancy_stmt)

                for vacancy in vacancies.unique():
                    vacancy_id = vacancy.id
                    post_stmt = select(Post).where(Post.vacancy_id == vacancy.id)
                    feedback_stmt = select(Feedback).where(Feedback.vacancy_id == vacancy.id)
                    posts = await session.scalars(post_stmt)
                    feedbacks = await session.scalars(feedback_stmt)
                    vacancy_name = vacancy.name
                    posts = posts.unique()
                    responses = feedbacks.unique()

                    reports.append(Reporting(
                        vacancy_id=vacancy_id,
                        vacancy_name=vacancy_name,
                        number_posts=len([post for post in posts]),
                        number_responses=len([response for response in responses])
                    ))
        return reports
