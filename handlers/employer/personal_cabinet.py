
import os
import pandas as pd
from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Text, StateFilter
from aiogram.types import Message, CallbackQuery

from keyboards.employer import customer_action_1, customer_action_2
from keyboards.employer import keyboard_employer_start, keyboard_url_button
from states.employer import FSMFormEvent


employer_pc_router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру с инлайн-кнопками
@employer_pc_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Выберете необходимое действие',
                         reply_markup=keyboard_employer_start)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_1_pressed' - Загрузить вакансии
@employer_pc_router.callback_query(Text(text=['big_button_1_pressed']))
async def process_button_1_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=f'Скачайте форму.\nЗаполните и направьте форму в бот для размещения вакансии.\n')
    await callback.message.answer(text='Скачать форму для заполнения.',
                                  reply_markup=keyboard_url_button)
    await state.set_state(FSMFormEvent.lreporting)


# Этот хэндлер будет срабатывать на отправку боту файла
@employer_pc_router.message(F.content_type == ContentType.DOCUMENT,
                            StateFilter(FSMFormEvent.lreporting))
async def download_document(message: Message, bot: Bot):
    await bot.download(
        message.document,
        destination=f"{message.document.file_id}vacancy.xlsx")
    df = pd.read_excel(f'{message.document.file_id}vacancy.xlsx')
    df.to_csv(f'{message.document.file_id}vacancy.csv', index=False)
    os.remove(f'{message.document.file_id}vacancy.xlsx')
    df = pd.read_csv(f'{message.document.file_id}vacancy.csv')
    vacancy_dict = {}
    for i in range(len(df)):
        vacancy_dict[i] = {'vacancy_name': df.loc[i, 'должность'],
                           'audience': df.loc[i, 'специализация'],
                           'employment': df.loc[i, 'тип занятости'],
                           'work_schedule': df.loc[i, 'график работы'],
                           'gender': df.loc[i, 'пол'],
                           'education': df.loc[i, 'образование'],
                           'salary': df.loc[i, 'размер заработной платы: руб.']}
    os.remove(f'{message.document.file_id}vacancy.csv')
    return vacancy_dict
# TODO Произвести запись в базу даных


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_2_pressed'
@employer_pc_router.callback_query(Text(text=['big_button_2_pressed']))
async def process_button_2_press(callback: CallbackQuery):
    if callback.message.text != f'Была нажата кнопка "{customer_action_2}"':
        await callback.message.edit_text(
            text=f'Была нажата кнопка "{customer_action_2}"',
            reply_markup=callback.message.reply_markup)
    await callback.answer(text=f'Ура! Нажата кнопка "{customer_action_2}"')



@employer_pc_router.message()
@employer_pc_router.callback_query()
async def process_start_command(message: Message):
    await message.answer("Вы что то делаете не так, перезапустите бот и попробуйте еще раз")
