from ..types import DAOFeedbackData
from sqlalchemy import select
from ..models import Feedback


class DAOFeedbackMixin:
    sql_manager = None

    async def insert_or_update_vacancy_response(self, vacancy_response: DAOFeedbackData) -> None:
        await self.sql_manager.create_async_session()
        async with self.sql_manager.async_session() as session:
            async with session.begin():
                stmt = select(Feedback).where(Feedback.vacancy_id == vacancy_response.vacancy_id).where(
                    Feedback.candidate_id == vacancy_response.candidate_id).where(
                    Feedback.deleted_at is not None)
                result = await session.scalars(stmt)
                tmp = result.first()
                if not tmp:
                    session.add(Feedback(**vacancy_response.__dict__))
                    session.commit()
                else:
                    feedback = tmp
                    feedback.vacancy_id = vacancy_response.vacancy_id
                    feedback.candidate_id = vacancy_response.vacancy_id
                    session.commit()
