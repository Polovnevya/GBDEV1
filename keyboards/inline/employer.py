<<<<<<< Updated upstream
from typing import Optional, Type
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.types import GenderEnum, EducationEnum, AgeCategoriesEnum


class PersonalData(CallbackData, prefix="PD"):
    action: str
    value: Optional[str]


def get_personal_data_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Да", callback_data=PersonalData(action="Yes", value="1")
    )
    builder.button(
        text=f"Нет", callback_data=PersonalData(action="No", value="0")
    )
    builder.adjust(2)
    return builder.as_markup()
=======
from typing import Optional
# , Type
from aiogram.filters.callback_data import CallbackData
# from aiogram.utils.keyboard import InlineKeyboardBuilder

# from db.models import GenderEnum, EducationEnum, AgeCategoriesEnum


class CompanyData(CallbackData, prefix="CD"):
    action: str
    value: Optional[str]
>>>>>>> Stashed changes
