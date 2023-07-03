from sqlalchemy import select
from ..models import Post


class DAOPostMixin:
    sql_manager = None

    async def insert_post(self, channel_id: int, message_id: int, vacancy_id: int):
        await self.sql_manager.create_async_session()
        async with self.sql_manager.async_session() as session:
            async with session.begin():
                stmt = select(Post).filter_by(vacancy_id=vacancy_id,
                                              channel_id=channel_id,
                                              message_id=message_id,
                                              )
                result = await session.scalar(stmt)

                if not result:
                    session.add(Post(vacancy_id=vacancy_id,
                                     channel_id=channel_id,
                                     message_id=message_id,
                                     ))
                    session.commit()
                else:
                    post = result
                    post.vacancy_id = vacancy_id
                    post.channel_id = channel_id
                    post.message_id = message_id
                    session.commit()
