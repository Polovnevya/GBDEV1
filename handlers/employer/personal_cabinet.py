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
from reporting import Reporting
from requests import request1, request2

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
    document = FSInputFile(path='files/work/common/vacancy_template.xlsx')
    await bot.send_document(callback.message.chat.id, document=document)
    await callback.message.answer(
        text=f'Скачайте форму.\nЗаполните и направьте форму в бот для размещения вакансии.\n')
    await callback.answer()
    await state.set_state(FSMFormEvent.lreporting)


# Этот хэндлер будет срабатывать на отправку боту файла
@employer_pc_router.message(F.content_type == ContentType.DOCUMENT,
                            StateFilter(FSMFormEvent.lreporting))
async def download_document(message: Message, bot: Bot):
    if not os.path.exists(f"files/downloads/{message.from_user.id}"):
        os.mkdir(f"files/downloads/{message.from_user.id}")
    if not os.path.exists(f"files/downloads/{message.from_user.id}/{message.date.strftime('%Y-%m-%d')}"):
        os.mkdir(f"files/downloads/{message.from_user.id}/{message.date.strftime('%Y-%m-%d')}")
    name_form = f"files/downloads/{message.from_user.id}/{message.date.strftime('%Y-%m-%d')}/{message.document.file_id}"
    await bot.download(
        message.document,
        destination=f'{name_form}.xlsx')
    try:
        df = pd.read_excel(f'{name_form}.xlsx')
        df.to_csv(f'{name_form}.csv', index=False)
        df = pd.read_csv(f'{name_form}.csv')
        vacancy_dict = {}
        for i in range(len(df)):
            vacancy_dict[i] = {'vacancy_name': df.loc[i, 'должность'],
                               'audience': df.loc[i, 'специализация'],
                               'employment': df.loc[i, 'тип занятости'],
                               'work_schedule': df.loc[i, 'график работы'],
                               'gender': df.loc[i, 'пол'],
                               'education': df.loc[i, 'образование'],
                               'salary': df.loc[i, 'размер заработной платы: руб.']}
        os.remove(f'{name_form}.csv')
        await message.answer("Файл поступил и обработан.")
        return vacancy_dict
    except ValueError:
        await message.answer(f'Вы направили файл иного формата.\n'
                             f'Заполните предоставленную форму и отправьте её в бот.')
        if os.path.isfile(f'{name_form}.xlsx'):
            os.remove(f'{name_form}.xlsx')
    except KeyError:
        await message.answer(f'Вы направили файл содержание котого не соответствует направленной вам форме для заполнения.\n'
                             f'Заполните предоставленную форму и отправьте её в бот.')
        if os.path.isfile(f'{name_form}.xlsx'):
            os.remove(f'{name_form}.xlsx')
        if os.path.isfile(f'{name_form}.csv'):
            os.remove(f'{name_form}.csv')
# TODO Произвести запись в базу даных


# Этот хэндлер будет срабатывать на отправку отчетности по размещённым вакансиям
@employer_pc_router.callback_query(EmployerReportingCB.filter())
async def process_button_2_press(callback: CallbackQuery, bot: Bot):
    request_list = []
    list_name_request = ['Количество откликов на вакансии:',
                         'Количество опубликованных постов с вакансией:']
    for elm in [request1, request2]:
        mod_request = elm + (f'WHERE employers.tg_id = {callback.from_user.id}\n'
                             f'GROUP BY vacancies.id')
        report = Reporting()
        records = report.get_reporting(mod_request)
        request_list.append(records)
        path_file_to_reporting = f'files/work/unloading/{callback.from_user.id}'
    if not os.path.exists(path_file_to_reporting):
        os.mkdir(path_file_to_reporting)
    for i in range(len(request_list)):
        with open(f'{path_file_to_reporting}/reporting.txt', 'a+', encoding="utf-8") as f:
            f.write(f'{list_name_request[i]}\n')
        for j in range(len(request_list[i])):
            with open(f'{path_file_to_reporting}/reporting.txt', 'a+', encoding="utf-8") as f:
                f.write(f'{request_list[i][j][0]}: {request_list[i][j][1]}\n')
                if j == len(request_list[i])-1:
                    f.write(f'\n')
    document = FSInputFile(path=f'{path_file_to_reporting}/reporting.txt')
    await bot.send_document(callback.message.chat.id, document=document)
    with open(f'{path_file_to_reporting}/reporting.txt', 'w') as f:
        pass


@employer_pc_router.message()
@employer_pc_router.callback_query()
async def process_start_command(message: Message):
    await message.answer("Вы что то делаете не так, перезапустите бот и попробуйте еще раз")
