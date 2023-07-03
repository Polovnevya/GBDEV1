from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


async def get_url_keyboard_fab(vacancy_id: int, bot: Bot):
    bot_info = await bot.me()
    bot_username = bot_info.username

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Откликнуться на вакансию",
        url=f"https://t.me/{bot_username}?start={vacancy_id}"
    ))
    builder.adjust(1)
    return builder.as_markup()
