from typing import Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import GenderEnum


class GenderCallbackFactory(CallbackData, prefix="GCF"):
    action: str
    value: Optional[int]


class AgeCallbackFactory(CallbackData, prefix="ACF"):
    action: str
    value: Optional[int]


class EducationCallbackFactory(CallbackData, prefix="ECF"):
    action: str
    value: Optional[int]


def get_gender_keyboard_fab(genders: GenderEnum):
    builder = InlineKeyboardBuilder()
    for gender in genders:
        builder.button(
        text=f"{gender.value}", callback_data=GenderCallbackFactory(action="GCF", value=gender)
    )
    # Выравниваем кнопки по 4 в ряд, чтобы получилось 4 + 1
    builder.adjust(4)
    return builder.as_markup()
