from typing import Union
from sqlalchemy import select
from ..models import Candidate
from ..types import DAOCandidateData


class DAOCandidateMixin:
    sql_manager = None

    # TODO запилить реализацию
    async def get_candidate_by_id(self, candidate_tg_id: int) -> Union[dict, None]:
        """
        ищет по tg_id кандидата, если он не удален
        :param candidate_tg_id:
        :return: возвращает данные кандидата в виде словаря если он имеется в таблице
                и None если такого кандидата в базе нет
        """

        await self.sql_manager.create_async_session()
        async with self.sql_manager.async_session() as session:
            async with session.begin():
                stmt = select(Candidate).where(Candidate.tg_id == candidate_tg_id).where(
                    Candidate.deleted_at is not None)
                result = await session.scalars(stmt)
                if result:
                    candidate = result.first()
                    return {'first_name': candidate.first_name,
                            'middle_name': candidate.middle_name,
                            'last_name': candidate.last_name,
                            'gender': candidate.gender.value,
                            'age': candidate.age.value,  # тут должны быть значения энамов, а не ключи
                            'education': candidate.education.value,
                            'phone': candidate.phone,
                            'tg_id': candidate.tg_id}

    # TODO запилить реализацию
    async def insert_or_update_candidate(self, candidate_data: DAOCandidateData) -> None:
        """
        Принимает dataclass с данными кандидата
        производит добавление кандидата если его нет
        и
        обновляет данные кандидата если он уже есть в базе
        можно разбить на 2 метода добавление и обновление, а этот использовать как фасад

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
                    session.commit()