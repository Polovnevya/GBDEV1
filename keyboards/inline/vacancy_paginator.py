import typing

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from aiogram.utils.keyboard import InlineKeyboardBuilder


class Navigation(CallbackData, prefix="PG"):
    direction: str


class VacancyResponse(CallbackData, prefix="VR"):
    id_vacancy: str


def get_vacancy_parinator_keyboard_fab(vacancy_data):
    builder = InlineKeyboardBuilder()
    vacancy: typing.Dict
    for vacancy in vacancy_data:
        builder.button(
            text="Откликнуться на вакансию",
            callback_data=VacancyResponse(id_vacancy=vacancy.get("id"))
        )
        builder.adjust(1)

    return Paginator(builder.as_markup())


#
class Paginator:
    def __init__(self, buttons: InlineKeyboardMarkup, buttons_on_page: int = 1) -> None:
        self.__buttons = buttons.inline_keyboard
        self.__buttons_on_page = buttons_on_page
        self.__current_page = 0
        self.page = 0

    async def update_kb(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        from_ = self.__current_page * self.__buttons_on_page
        to_ = (self.__current_page + 1) * self.__buttons_on_page

        for button in self.__buttons[from_:to_]:
            builder.button(text=button[0].text, callback_data=button[0].callback_data)
            builder.adjust(1)

        if len(self.__buttons) > self.__buttons_on_page:
            if from_ <= 0:
                builder.button(text="Еще ▶", callback_data=Navigation(direction="next"))
                builder.adjust(1)
                return builder.as_markup()

            elif to_ >= len(self.__buttons):
                builder.button(text="◀ Назад", callback_data=Navigation(direction="previous"))
                builder.adjust(1)
                return builder.as_markup()

            buttons: typing.List[InlineKeyboardButton] = [
                InlineKeyboardButton(text="◀ Назад", callback_data="PG:previous"),
                InlineKeyboardButton(text="Еще ▶", callback_data="PG:next"), ]
            builder.row(*buttons)
            return builder.as_markup()

        else:
            return builder.as_markup()

    async def on_next(self) -> None:
        self.__current_page += 1
        self.page += 1

    async def on_prev(self) -> None:
        self.__current_page -= 1
        self.page -= 1
