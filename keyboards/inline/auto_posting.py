from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_url_keyboard_fab(vacancy_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Откликнуться на вакансию",
        url=f"https://t.me/funny_prediction_zodiac_bot?start={vacancy_id}"
    ))
    builder.adjust(1)
    return builder.as_markup()
