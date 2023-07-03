from typing import List
from sqlalchemy import select
from ..models import Channel, Audience


class DAOChannelMixin:
    sql_manager = None

    async def get_channels_id_by_audience(self, audience_id: int) -> List[int]:
        await self.sql_manager.create_async_session()
        async with self.sql_manager.async_session() as session:
            async with session.begin():
                channels = await session.scalars(select(Channel).where(Channel.audience.any(id=audience_id)))

        return [channel.channel_id for channel in channels.unique()]


