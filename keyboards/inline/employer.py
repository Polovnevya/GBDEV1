from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class EmployerLoadCB(CallbackData, prefix="ELCB"):
    value: str


class EmployerReportingCB(CallbackData, prefix="ERCB"):
    value: str


def get_start_employer_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Загрузить вакансии", callback_data=EmployerLoadCB(value="load")
    )
    builder.button(
        text=f"Выгрузить отчётность", callback_data=EmployerReportingCB(value="reporting")
    )
    builder.adjust(1)
    return builder.as_markup()
