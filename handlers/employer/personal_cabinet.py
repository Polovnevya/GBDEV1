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
from db.types import DAOVacancyData, WorkScheduleEnum, EmploymentEnum, AudienceEnum
from loader import db
import datetime

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
        # vacancy_dict = {}
        for i in range(len(df)):
            await db.insert_vacancy(
                DAOVacancyData(employer_id=await db.get_employer_id_by_tguser_id(message.from_user.id),
                               audience_id=await db.get_audience_id_by_name(AudienceEnum(df.loc[i, 'специализация'])),
                               name=df.loc[i, 'должность'],
                               work_schedule=WorkScheduleEnum(df.loc[i, 'график работы']),
                               employment=EmploymentEnum(df.loc[i, 'тип занятости']),
                               salary=float(df.loc[i, 'размер заработной платы: руб.']),
                               geolocation='69.333333, 88.333333',
                               is_open=True,
                               date_start=datetime.datetime.now(),
                               date_end=datetime.datetime.now()+datetime.timedelta(days=10)
                               )
                               )
        os.remove(f'{name_form}.csv')
        await message.answer("Файл поступил и обработан.")
        # return vacancy_dict
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
async def process_button_2_press(callback: CallbackQuery,
                                 bot: Bot,):
    report = Reporting()
    records = report.get_reporting(f'WITH\n'
                                   f'number_responses AS (\n'
                                        f'SELECT vacancies.id, COUNT(candidates.id) AS count_responses\n'
                                        f'FROM employers\n'
                                        f'JOIN vacancies ON employers.id = vacancies.employer_id\n'
                                        f'JOIN feedback ON vacancies.id = feedback.vacancy_id\n'
                                        f'JOIN candidates ON feedback.candidate_id = candidates.id\n'
                                        f'WHERE employers.tg_id = 3\n'
                                        f'GROUP BY vacancies.id),\n'
                                    f'number_posts AS (\n'
                                        f'SELECT vacancies.id AS id, vacancies.name AS name, COUNT(posts.id) AS count_posts\n'
                                        f'FROM posts\n'
                                        f'JOIN vacancies ON posts.vacancy_id = vacancies.id\n'
                                        f'JOIN employers ON employers.id = vacancies.employer_id\n'
                                        f'WHERE employers.tg_id = {callback.from_user.id}\n'
                                        f'GROUP BY vacancies.id)\n'
                                    f'SELECT number_posts.id, number_posts.name, number_posts.count_posts, number_responses.count_responses\n'
                                    f'FROM number_posts LEFT OUTER JOIN number_responses ON number_posts.id=number_responses.id;'
                                    )
    list_name_request = [('id',
                          'Наименование вакансии',
                          'Количество опубликованных постов с вакансией',
                          'Количество откликов на вакансию',)]
    list_name_request.extend(records)

    path_file_to_reporting = f'files/work/unloading/{callback.from_user.id}'
    if not os.path.exists(path_file_to_reporting):
        os.mkdir(path_file_to_reporting)
    for i in range(len(list_name_request)):
        with open(f'{path_file_to_reporting}/reporting.csv', 'a+', encoding="utf-8") as f:
            f.write(f'{",".join(map(str, list_name_request[i]))}\n')
    df = pd.read_csv(f'{path_file_to_reporting}/reporting.csv')
    df.to_excel(f'{path_file_to_reporting}/Отчёт.xlsx', engine='openpyxl')
    document = FSInputFile(path=f'{path_file_to_reporting}/Отчёт.xlsx')
    await callback.message.answer(text='Отчет сформирован.')
    await bot.send_document(callback.message.chat.id, document=document)
    with open(f'{path_file_to_reporting}/reporting.csv', 'w') as f:
        pass


@employer_pc_router.message()
@employer_pc_router.callback_query()
async def process_start_command(message: Message):
    await message.answer("Вы что то делаете не так, перезапустите бот и попробуйте еще раз")
