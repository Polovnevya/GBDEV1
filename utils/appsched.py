import asyncio
from typing import List

from aiogram import Bot

from db.sql_facade import DAO
from db.types import DAOVacancyData
from keyboards.inline.auto_posting import get_url_keyboard_fab


async def __send_message_2_channel(bot: Bot, vacancy: DAOVacancyData, tg_channel_id: int) -> int:
    result = await bot.send_message(tg_channel_id,
                                    f"Условия {vacancy.name}\n"
                                    f"График {vacancy.work_schedule.value}\n"
                                    f"Оплата {vacancy.salary}",
                                    reply_markup=await get_url_keyboard_fab(vacancy.id, bot))
    return result.message_id


async def auto_posting(bot: Bot, db: DAO):
    vacancies = await db.get_vacancy_by_geolocation()
    for vacancy in vacancies:
        channels = await db.get_channels_id_by_audience(vacancy.audience_id)
        for channel_id in channels:
            await asyncio.sleep(0.3)
            post_id = await __send_message_2_channel(bot, vacancy, channel_id)
            await db.insert_post(channel_id=channel_id, message_id=post_id, vacancy_id=vacancy.id)
