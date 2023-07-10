import datetime
import os
from typing import List

import pandas as pd
from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove

from config.config import config
from db.types import DAOVacancyData, WorkScheduleEnum, EmploymentEnum, AudienceEnum
from db.types import ReportingPostsResponses, ReportingVacancy
from filters.employer import IsEmployer
from keyboards.inline.employer import get_start_employer_keyboard, EmployerLoadCB, EmployerReportingCB
from loader import db
from states.employer import FSMFormEvent
from openpyxl.workbook import Workbook

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
        text=f'Скачайте форму.\nЗаполните и направьте форму в бот для размещения вакансии.\n',
        reply_markup=ReplyKeyboardRemove())
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
        os.remove(f'{name_form}.csv')

    except ValueError:
        await message.answer(f'Вы направили файл иного формата.\n'
                             f'Заполните предоставленную форму и отправьте её в бот.')
        if os.path.isfile(f'{name_form}.xlsx'):
            os.remove(f'{name_form}.xlsx')
        df = []
    except KeyError:
        await message.answer(
            f'Вы направили файл содержание котого не соответствует направленной вам форме для заполнения.\n'
            f'Заполните предоставленную форму и отправьте её в бот.')
        if os.path.isfile(f'{name_form}.xlsx'):
            os.remove(f'{name_form}.xlsx')
        if os.path.isfile(f'{name_form}.csv'):
            os.remove(f'{name_form}.csv')

    validated_vacancy = []

    for i in range(len(df)):
        try:
            audience_id = await db.get_audience_id_by_name(AudienceEnum(df.loc[i, 'специализация']))
        except KeyError:
            await message.answer(f'В вакансии на строке №{i + 1} ошибка в столбце "специализация"!\n'
                                 f'Заполните предоставленную форму в соответствии с требованиями и отправьте её в бот.\n')
            if os.path.isfile(f'{name_form}.xlsx'):
                os.remove(f'{name_form}.xlsx')
            if os.path.isfile(f'{name_form}.csv'):
                os.remove(f'{name_form}.csv')
            break

        try:
            work_schedule = WorkScheduleEnum(df.loc[i, 'график работы'])
        except KeyError:
            await message.answer(f'В вакансии на строке №{i + 1} ошибка в столбце "График работы"!\n'
                                 f'Заполните предоставленную форму в соответствии с требованиями и отправьте её в бот.\n')
            if os.path.isfile(f'{name_form}.xlsx'):
                os.remove(f'{name_form}.xlsx')
            if os.path.isfile(f'{name_form}.csv'):
                os.remove(f'{name_form}.csv')

        try:
            employment = EmploymentEnum(df.loc[i, 'тип занятости'])
        except KeyError:
            await message.answer(f'В вакансии на строке №{i + 1} ошибка в столбце "тип занятости"!\n'
                                 f'Заполните предоставленную форму в соответствии с требованиями и отправьте её в бот.\n')
            if os.path.isfile(f'{name_form}.xlsx'):
                os.remove(f'{name_form}.xlsx')
            if os.path.isfile(f'{name_form}.csv'):
                os.remove(f'{name_form}.csv')
            break

        try:
            salary = float(df.loc[i, 'размер заработной платы: руб.'])
        except KeyError:
            await message.answer(
                f'В вакансии на строке №{i + 1} ошибка в столбце "размер заработной платы: руб."!\n'
                f'Заполните предоставленную форму в соответствии с требованиями и отправьте её в бот.\n')
            if os.path.isfile(f'{name_form}.xlsx'):
                os.remove(f'{name_form}.xlsx')
            if os.path.isfile(f'{name_form}.csv'):
                os.remove(f'{name_form}.csv')
            break

        validated_vacancy.append(
            DAOVacancyData(employer_id=await db.get_employer_id_by_tguser_id(message.from_user.id),
                           audience_id=audience_id,
                           name=df.loc[i, 'должность'],
                           work_schedule=work_schedule,
                           employment=employment,
                           salary=salary,
                           geolocation='69.333333, 88.333333',
                           is_open=True,
                           date_start=datetime.datetime.now(),
                           date_end=datetime.datetime.now() + datetime.timedelta(days=10)
                           ))

    for vacancy in validated_vacancy:
        await db.insert_vacancy(vacancy)
    await message.answer("Файл поступил и обработан.")


# Этот хэндлер будет срабатывать на отправку отчетности по размещённым вакансиям
# количество опубликованных постов с вакансией и отклики на вакансию
@employer_pc_router.callback_query(EmployerReportingCB.filter())
async def process_button_2_press(callback: CallbackQuery,
                                 bot: Bot, ):
    records1: List[ReportingPostsResponses] = await db.get_reporting(
        await db.get_employer_id_by_tguser_id(callback.from_user.id))
    records2: List[ReportingVacancy] = await db.get_reporting_response_vacancy(
        await db.get_employer_id_by_tguser_id(callback.from_user.id))
    list_name_request1 = []
    list_name_request2 = []
    name_title1 = [('id',
                    'Наименование вакансии',
                    'Количество опубликованных постов с вакансией',
                    'Количество откликов на вакансию',)]
    name_title2 = [('id',
                    'Наименование вакансии',
                    'Количество откликов со стороны мужчин',
                    'Количество откликов со стороны женщин',
                    'Количество откликов кандидатов категории junior',
                    'Количество откликов кандидатов категории middle',
                    'Количество откликов кандидатов категории senior',
                    'Количество откликов кандидатов со средним образованием',
                    'Количество откликов кандидатов со средним профессиональным образованием',
                    'Kоличество откликов кандидатов с высшим образованием')]
    for i in range(len(records1)):
        list_name_request1.append((records1[i].vacancy_id,
                                   records1[i].vacancy_name,
                                   records1[i].number_posts,
                                   records1[i].number_responses)
                                  )

    for i in range(len(records2)):
        list_name_request2.append((records2[i].vacancy_id,
                                   records2[i].vacancy_name,
                                   records2[i].male,
                                   records2[i].female,
                                   records2[i].junior,
                                   records2[i].middle,
                                   records2[i].senior,
                                   records2[i].secondary,
                                   records2[i].vocational,
                                   records2[i].higher)
                                  )

    path_file_to_reporting = f'files/work/unloading/{callback.from_user.id}'
    if not os.path.exists(path_file_to_reporting):
        os.mkdir(path_file_to_reporting)

    wb = Workbook()
    list1 = wb.active
    list1.title = 'Отчёт №1'
    list2 = wb.create_sheet('Отчёт №2')
    list_name_title = [name_title1, name_title2]
    list_name_request = [list_name_request1, list_name_request2]
    sheet_names = ['Отчёт №1', 'Отчёт №2']
    list_sheet = [list1, list2]
    for i in range(len(sheet_names)):
        list_sheet[i] = wb[sheet_names[i]]
        list_sheet[i].append(list_name_title[i][0])
        for row in list_name_request[i]:
            list_sheet[i].append(row)
    wb.save(f'{path_file_to_reporting}/Отчёт.xlsx')

    document = FSInputFile(path=f'{path_file_to_reporting}/Отчёт.xlsx')
    await callback.message.answer(text='Отчет сформирован.')
    await bot.send_document(callback.message.chat.id, document=document)
