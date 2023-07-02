from typing import Dict, List

from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ChatInviteLink

from db.models import GenderEnum, AgeCategoriesEnum, EducationEnum
from db.types import DAOFeedbackData, DAOVacancyData, DAOCandidateData
from keyboards.candidate import kb_contact, kb_geo
from keyboards.inline.candidate import (
    get_gender_keyboard_fab, GenderCallback, AgeCallback, get_age_keyboard_fab,
    EducationCallback, get_education_keyboard_fab, get_personal_data_keyboard, PersonalData, )
from keyboards.inline.vacancy_paginator import Paginator, Navigation, \
    VacancyResponse, get_vacancy_paginator_keyboard_fab
from loader import db
from states.candidate import FSMCandidatePoll
from utils.appsched import auto_posting

candidate_pc_router: Router = Router()


@candidate_pc_router.message(Command(commands=['start']))  # , StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext, command: CommandObject):
    args = command.args
    await state.clear()
    await message.answer(f"Добрый день {message.from_user.full_name}!\n"
                         f"Для создания отклика пройдите небольшой анкетирование",
                         reply_markup=ReplyKeyboardRemove())

    result: DAOCandidateData = await db.get_candidate_by_id(message.from_user.id)
    if not result:
        await message.answer(f"Введите Ваше имя")
        await state.set_state(FSMCandidatePoll.first_name)
    else:
        await message.answer(f"Это корректные данные?\n"
                             f"Имя: {result.first_name} \n"
                             f"Отчество: {result.middle_name} \n"
                             f"Фамилия: {result.last_name} \n"
                             f"Пол: {result.gender} \n"
                             f"Возраст: {result.age} \n"
                             f"Образование: {result.education} \n"
                             f"Телефон: {result.phone}",
                             reply_markup=get_personal_data_keyboard())
        await state.set_state(FSMCandidatePoll.load_pd)


@candidate_pc_router.callback_query(PersonalData.filter(), StateFilter(FSMCandidatePoll.load_pd))
async def process_candidate_pd(query: CallbackQuery, callback_data: EducationCallback, state: FSMContext):
    if callback_data.value == '0':
        await state.clear()
        await query.answer()
        await query.message.answer(f"Добрый день {query.from_user.full_name}!\n"
                                   f"Для создания отклика пройдите небольшой анкетирование")
        await query.message.answer(f"Введите Ваше имя", reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSMCandidatePoll.first_name)
    else:
        await query.message.answer("Для дальнейшего поиска открытых вакансий - "
                                   "отправьте свою геолокацию и бот подберет для вас самые ближайшие варианты",
                                   reply_markup=kb_geo)

        await state.set_state(FSMCandidatePoll.geolocation)


@candidate_pc_router.message(F.text, StateFilter(FSMCandidatePoll.first_name))
async def process_get_first_name(message: Message, state: FSMContext):
    await state.update_data({"first_name": message.text})
    await message.answer(f"Введите Ваше отчество")
    await state.set_state(FSMCandidatePoll.middle_name)


@candidate_pc_router.message(F.text, StateFilter(FSMCandidatePoll.middle_name))
async def process_get_middle_name(message: Message, state: FSMContext):
    await state.update_data({"middle_name": message.text})
    await message.answer(f"Введите Вашу фамилию")
    await state.set_state(FSMCandidatePoll.last_name)


@candidate_pc_router.message(F.text, StateFilter(FSMCandidatePoll.last_name))
async def process_get_last_name(message: Message, state: FSMContext):
    await state.update_data({"last_name": message.text})
    await message.answer(f"Выберете Ваш пол",
                         reply_markup=get_gender_keyboard_fab(GenderEnum))
    await state.set_state(FSMCandidatePoll.gender)


@candidate_pc_router.callback_query(GenderCallback.filter(), StateFilter(FSMCandidatePoll.gender))
async def process_get_gender(query: CallbackQuery, callback_data: GenderCallback, state: FSMContext):
    await state.update_data({"gender": callback_data.value})
    await query.message.answer(f"Выберете Ваш возраст",
                               reply_markup=get_age_keyboard_fab(AgeCategoriesEnum))
    await state.set_state(FSMCandidatePoll.age)


@candidate_pc_router.callback_query(AgeCallback.filter(), StateFilter(FSMCandidatePoll.age))
async def process_get_age(query: CallbackQuery, callback_data: AgeCallback, state: FSMContext):
    await state.update_data({"age": callback_data.value})
    await query.message.answer(f"Выберете Ваше образование",
                               reply_markup=get_education_keyboard_fab(EducationEnum))
    await state.set_state(FSMCandidatePoll.education)


@candidate_pc_router.callback_query(EducationCallback.filter(), StateFilter(FSMCandidatePoll.education))
async def process_get_education(query: CallbackQuery, callback_data: EducationCallback, state: FSMContext):
    await state.update_data({"education": callback_data.value})
    await query.message.answer("Отправьте свой номер телефона", reply_markup=kb_contact)
    await state.set_state(FSMCandidatePoll.phone)


@candidate_pc_router.message(StateFilter(FSMCandidatePoll.phone), F.content_type.in_({ContentType.CONTACT}))
async def process_get_phone(message: Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await state.update_data({"tg_id": message.from_user.id})
    # тут записываем в базу данных
    data = await state.get_data()
    await db.insert_or_update_candidate(
        DAOCandidateData(first_name=data.get("first_name"),
                         middle_name=data.get("middle_name"),
                         last_name=data.get("last_name"),
                         gender=data.get("gender"),
                         age=data.get("age"),
                         education=data.get("education"),
                         phone=data.get("phone"),
                         tg_id=data.get("tg_id")))
    await message.answer("Спасибо что прошли опрос!\n"
                         "Для дальнейшего поиска открытых вакансий - "
                         "отправьте свою геолокацию и бот подберет для вас самые ближайшие варианты",
                         reply_markup=kb_geo)
    await state.set_state(FSMCandidatePoll.geolocation)


@candidate_pc_router.message(StateFilter(FSMCandidatePoll.geolocation), F.content_type.in_({ContentType.LOCATION}))
async def process_show_vacancy(message: Message, state: FSMContext, bot: Bot):
    longitude: float = message.location.longitude
    latitude: float = message.location.latitude
    result: List[DAOVacancyData] = await db.get_vacancy_by_geolocation(longitude, latitude)
    await state.set_state(FSMCandidatePoll.show_vacancy)
    await state.update_data({"vacancy": result})
    await state.update_data({"paginator": result})

    vacancy_paginator: Paginator = get_vacancy_paginator_keyboard_fab(result)
    await state.update_data({"paginator": vacancy_paginator})
    current_vacancy_data: DAOVacancyData = result[0]
    a = await auto_posting(db=db, bot=bot)

    await message.answer(f"Текст вакансии: {current_vacancy_data.name}\n"
                         f"Оплата: {current_vacancy_data.salary}\n"
                         f"График: {current_vacancy_data.work_schedule.value}\n",
                         reply_markup=await vacancy_paginator.update_kb())


@candidate_pc_router.callback_query(StateFilter(FSMCandidatePoll.show_vacancy),
                                    VacancyResponse.filter())
async def process_vacancy_response(query: CallbackQuery, callback_data: VacancyResponse):
    id_vacancy: int = int(callback_data.id_vacancy)
    # записываем отклик в базу
    result: DAOCandidateData = await db.get_candidate_by_id(query.from_user.id)
    await db.insert_or_update_vacancy_response(DAOFeedbackData(candidate_id=result.id,
                                                               vacancy_id=id_vacancy))
    await query.answer("Отклик создан")
    # TODO добавить описание вакансии
    await query.message.answer("Отклик создан")


#
@candidate_pc_router.callback_query(StateFilter(FSMCandidatePoll.show_vacancy),
                                    Navigation.filter(F.direction == "next"))
async def process_forward_show_vacancy(query: CallbackQuery, state: FSMContext):
    result = await state.get_data()
    vacancy_paginator: Paginator = result.get("paginator")
    await vacancy_paginator.on_next()
    await state.update_data({"paginator": vacancy_paginator})
    current_vacancy_data: Dict = result.get("vacancy")[vacancy_paginator.page]
    await query.message.edit_text(f"Текст вакансии: {current_vacancy_data.name}\n"
                                  f"Оплата: {current_vacancy_data.salary}\n"
                                  f"График: {current_vacancy_data.work_schedule.value}\n",
                                  reply_markup=await vacancy_paginator.update_kb())


@candidate_pc_router.callback_query(StateFilter(FSMCandidatePoll.show_vacancy),
                                    Navigation.filter(F.direction == "previous"))
async def process_backward_show_vacancy(query: CallbackQuery, state: FSMContext):
    result = await state.get_data()
    vacancy_paginator: Paginator = result.get("paginator")
    await vacancy_paginator.on_prev()
    await state.update_data({"paginator": vacancy_paginator})
    current_vacancy_data: Dict = result.get("vacancy")[vacancy_paginator.page]
    await query.message.edit_text(f"Текст вакансии: {current_vacancy_data.name}\n"
                                  f"Оплата: {current_vacancy_data.salary}\n"
                                  f"График: {current_vacancy_data.work_schedule.value}\n",
                                  reply_markup=await vacancy_paginator.update_kb())


@candidate_pc_router.message(StateFilter(FSMCandidatePoll.geolocation))
async def process_show_vacancy_without_geo(message: Message):
    await message.answer(f"Отправьте свою геолокацию\n"
                         f"данная функция работает только на мобильном телефоне")


@candidate_pc_router.message()
@candidate_pc_router.callback_query()
async def process_start_command(query: CallbackQuery):
    a = 1
    # candidate = await db.get_candidate_by_id(618432846)
    # print(candidate)
    try:
        await query.message.answer("Вы что то делаете не так, перезапустите бот и попробуйте еще раз")
    except:
        await query.message.answer("Вы что то делаете не так, перезапустите бот и попробуйте еще раз")
