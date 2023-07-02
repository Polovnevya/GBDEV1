from aiogram import Bot

from db.types import DAOVacancyData


async def send_message_2_channel(bot: Bot, vacancy: DAOVacancyData) -> int:
    result = await bot.send_message(-1001829933123, #vacancy.audience_id,
                                    f"тут вакансия")
    a = result
    return result
