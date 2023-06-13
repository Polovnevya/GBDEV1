from typing import Optional, Type
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import GenderEnum, EducationEnum, AgeCategoriesEnum


class PersonalData(CallbackData, prefix="PD"):
    action: str
    value: Optional[str]


class GenderCallback(CallbackData, prefix="GC"):
    action: str
    value: Optional[str]


class AgeCallback(CallbackData, prefix="AC"):
    action: str
    value: Optional[str]


class EducationCallback(CallbackData, prefix="EC"):
    action: str
    value: Optional[str]


def get_education_keyboard_fab(educations: Type[EducationEnum]):
    builder = InlineKeyboardBuilder()
    for education in educations:
        builder.button(
            text=f"{education.value}", callback_data=EducationCallback(action="EC", value=education.name)
        )
    builder.adjust(1)
    return builder.as_markup()


def get_age_keyboard_fab(ages: Type[AgeCategoriesEnum]):
    builder = InlineKeyboardBuilder()
    for age in ages:
        builder.button(
            text=f"{age.value}", callback_data=AgeCallback(action="AC", value=age.name)
        )
    builder.adjust(1)
    return builder.as_markup()


def get_gender_keyboard_fab(genders: Type[GenderEnum]):
    builder = InlineKeyboardBuilder()
    for gender in genders:
        builder.button(
            text=f"{gender.value}", callback_data=GenderCallback(action="GC", value=gender.name)
        )
    builder.adjust(1)
    return builder.as_markup()


def get_personal_data_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Да", callback_data=PersonalData(action="Yes", value="1")
    )
    builder.button(
        text=f"Нет", callback_data=PersonalData(action="No", value="0")
    )
    builder.adjust(1)
    return builder.as_markup()
