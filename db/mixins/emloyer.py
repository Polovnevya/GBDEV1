from typing import Union, List
from sqlalchemy import select
from ..models import Employer, Vacancy, Post, Feedback, Candidate
from ..types import DAOEmployerData, ReportingPostsResponses, ReportingVacancy, GenderEnum, AgeCategoriesEnum, \
    EducationEnum


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

    async def get_reporting(self, employer_id: int) -> List[ReportingPostsResponses]:
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

                    reports.append(ReportingPostsResponses(
                        vacancy_id=vacancy_id,
                        vacancy_name=vacancy_name,
                        number_posts=len([post for post in posts]),
                        number_responses=len([response for response in responses])
                    ))
        return reports

    async def get_employer_id_by_tguser_id(self, tg_id: int) -> int:
        await self.sql_manager.create_async_session()
        async with self.sql_manager.async_session() as session:
            async with session.begin():
                employer = await session.scalar(select(Employer).filter_by(tg_id=tg_id))
        return employer.id

    async def get_reporting_response_vacancy(self, employer_id: int) -> list[ReportingVacancy]:
        """
        Возвращает список кортежей.
        Каждый кортеж содержит:
        - id вакансии;
        - наименование вакансии,
        - количество откликов со стороны мужчин,
        - количество откликов со стороны женщин,
        - количество откликов кандидатов категории junior,
        - количество откликов кандидатов категории middle,
        - количество откликов кандидатов категории senior,
        - количество откликов кандидатов со средним образованием,
        - количество откликов кандидатов со средним профессиональным образованием,
        - количество откликов кандидатов с высшим образованием

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
                    vacancy_name = vacancy.name
                    feedback_stmt = select(Feedback).where(Feedback.vacancy_id == vacancy.id)
                    feedback_by_male_stmt = select(Feedback).where(Feedback.vacancy_id == vacancy.id).join(
                        Candidate).where(Candidate.gender == GenderEnum.male)
                    feedback_by_female_stmt = select(Feedback).where(Feedback.vacancy_id == vacancy.id).join(
                        Candidate).where(Candidate.gender == GenderEnum.female)
                    feedback_by_junior_stmt = select(Feedback).where(Feedback.vacancy_id == vacancy.id).join(
                        Candidate).where(Candidate.age == AgeCategoriesEnum.junior)
                    feedback_by_middle_stmt = select(Feedback).where(Feedback.vacancy_id == vacancy.id).join(
                        Candidate).where(Candidate.age == AgeCategoriesEnum.middle)
                    feedback_by_senior_stmt = select(Feedback).where(Feedback.vacancy_id == vacancy.id).join(
                        Candidate).where(Candidate.age == AgeCategoriesEnum.senior)
                    feedback_by_secondary_stmt = select(Feedback).where(Feedback.vacancy_id == vacancy.id).join(
                        Candidate).where(Candidate.education == EducationEnum.secondary)
                    feedback_by_vocational_stmt = select(Feedback).where(Feedback.vacancy_id == vacancy.id).join(
                        Candidate).where(Candidate.education == EducationEnum.vocational)
                    feedback_by_higher_stmt = select(Feedback).where(Feedback.vacancy_id == vacancy.id).join(
                        Candidate).where(Candidate.education == EducationEnum.higher)

                    feedbacks = await session.scalars(feedback_stmt)
                    male = await session.scalars(feedback_by_male_stmt)
                    female = await session.scalars(feedback_by_female_stmt)
                    junior = await session.scalars(feedback_by_junior_stmt)
                    middle = await session.scalars(feedback_by_middle_stmt)
                    senior = await session.scalars(feedback_by_senior_stmt)
                    secondary = await session.scalars(feedback_by_secondary_stmt)
                    vocational = await session.scalars(feedback_by_vocational_stmt)
                    higher = await session.scalars(feedback_by_higher_stmt)

                    feedbacks = feedbacks.first()
                    male = male.unique()
                    female = female.unique()
                    junior = junior.unique()
                    middle = middle.unique()
                    senior = senior.unique()
                    secondary = secondary.unique()
                    vocational = vocational.unique()
                    higher = higher.unique()

                    if feedbacks:
                        reports.append(ReportingVacancy(
                            vacancy_id=vacancy_id,
                            vacancy_name=vacancy_name,
                            male=len([_ for _ in male]),
                            female=len([_ for _ in female]),
                            junior=len([_ for _ in junior]),
                            middle=len([_ for _ in middle]),
                            senior=len([_ for _ in senior]),
                            secondary=len([_ for _ in secondary]),
                            vocational=len([_ for _ in vocational]),
                            higher=len([_ for _ in higher])
                        ))
        return reports

