from typing import Union
from sqlalchemy import select
from ..models import Employer
from ..types import DAOEmployerData


class DAOEmployerMixin:
    sql_manager = None

    async def get_active_employers_by_id(self, employer_tg_id: int) -> Union[DAOEmployerData, bool]:
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
                if result.first():
                    employer = result.first()
                    return DAOEmployerData(
                        company_name=employer.company_name,
                        email=employer.email,
                        phone=employer.phone,
                        tg_id=employer.tg_id,
                    )
