import os
import pandas as pd
from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile
from config.config import config
from filters.employer import IsEmployer
from keyboards.inline.employer import get_start_employer_keyboard, EmployerLoadCB, EmployerReportingCB
from states.employer import FSMFormEvent

employer_pc_router: Router = Router()
employer_pc_router.message.filter(IsEmployer(config.employers.employers_ids))


# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру с инлайн-кнопками
@employer_pc_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Выберете необходимое действие',
                         reply_markup=get_start_employer_keyboard())


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_1_pressed' - Загрузить вакансии
@employer_pc_router.callback_query(EmployerLoadCB.filter())
async def process_button_load_press(callback: CallbackQuery, state: FSMContext, bot: Bot):
    document = FSInputFile(path='GBDEV1/files/work/common/vacancy_template.xlsx')
    await bot.send_document(callback.message.chat.id, document=document)
    await callback.message.answer(
        text=f'Скачайте форму.\nЗаполните и направьте форму в бот для размещения вакансии.\n')
    await callback.answer()
    await state.set_state(FSMFormEvent.lreporting)


# Этот хэндлер будет срабатывать на отправку боту файла
@employer_pc_router.message(F.content_type == ContentType.DOCUMENT,
                            StateFilter(FSMFormEvent.lreporting))
async def download_document(message: Message, bot: Bot):
    await bot.download(
        message.document,
        destination=f"{message.document.file_id}vacancy.xlsx")
    try:
        df = pd.read_excel(f'{message.document.file_id}vacancy.xlsx')
        df.to_csv(f'{message.document.file_id}vacancy.csv', index=False)
        # os.remove(f'{message.document.file_id}vacancy.xlsx')
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
        await message.answer("Файл поступил и обработан.")
        return vacancy_dict
    except ValueError:
        await message.answer(f'Вы направили файл иного формата.\n'
                             f'Заполните предоставленную форму и отправьте её в бот.')
    except KeyError:
        await message.answer(f'Вы направили файл содержание котого не соответствует направленной вам форме для заполнения.\n'
                             f'Заполните предоставленную форму и отправьте её в бот.')
        if os.path.isfile(f'{message.document.file_id}vacancy.csv'):
            os.remove(f'{message.document.file_id}vacancy.csv')
# TODO Произвести запись в базу даных


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_2_pressed'
@employer_pc_router.callback_query(EmployerReportingCB.filter())
async def process_button_2_press(callback: CallbackQuery, callback_data: EmployerReportingCB):
    if callback.message.text != f'Была нажата кнопка "{callback_data.value}"':
        await callback.message.edit_text(
            text=f'Была нажата кнопка "{callback_data.value}"',
            reply_markup=callback.message.reply_markup)
    await callback.answer(text=f'Ура! Нажата кнопка "{callback_data.value}"')


@employer_pc_router.message()
@employer_pc_router.callback_query()
async def process_start_command(message: Message):
    await message.answer("Вы что то делаете не так, перезапустите бот и попробуйте еще раз")
