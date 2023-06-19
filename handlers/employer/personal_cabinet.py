from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
# from db.models import GenderEnum, AgeCategoriesEnum, EducationEnum
from keyboards.candidate import kb_contact, kb_geo
from keyboards.inline.employer import get_personal_data_keyboard, PersonalData
from keyboards.inline.candidate import EducationCallback
from loader import db
from states.employer import FSMEmployerPoll
from keyboards.employer import keyboard


employer_pc_router: Router = Router()

@employer_pc_router.message(Command(commands=['bot']))  # , StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext, ):
    await state.clear()
    await message.answer(f"Добрый день {message.from_user.full_name}!\n"
                         f"Для создания вакансии необходимо заполнить\n"
                         f"форму и направте её боту",
                         reply_markup=ReplyKeyboardRemove())

    # TODO если кандидат уже есть в базе - пропускаем анкетирование,
    result = await db.get_active_employers_by_id(message.from_user.id)

    # await message.answer_document(open("Форма.xlsx"))
    #await state.set_state(FSMEmployerPoll.company_name)

    if not result:
        await message.answer(f"Введите наименование организации")
        await state.set_state(FSMEmployerPoll.company_name)
    else:
        await message.answer(f"Это корректные данные?\n"
                             f"Компании: {result.get('company_name')} \n"
                             f"Email: {result.get('email')} \n"
                             f"Телефон: {result.get('phone')}",
                             reply_markup=get_personal_data_keyboard())
        await state.set_state(FSMEmployerPoll.load_pd)


@employer_pc_router.callback_query(PersonalData.filter(), StateFilter(FSMEmployerPoll.load_pd))
async def process_candidate_pd(query: CallbackQuery, callback_data: EducationCallback, state: FSMContext):
    if callback_data.value == '0':
        await state.clear()
        await query.answer()
        await query.message.answer(#f"Добрый день {query.from_user.full_name}!\n"
                                   f"Для размещения вакансии пройдите небольшой анкетирование")
        await query.message.answer(f"Введите наименование компании", reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSMEmployerPoll.company_name)
    else:
        await query.message.answer("Отправьте свою геолокацию", reply_markup=kb_geo)

        await state.set_state(FSMEmployerPoll.geolocation)


@employer_pc_router.message(F.text, StateFilter(FSMEmployerPoll.company_name))
async def process_get_company_name(message: Message, state: FSMContext):
    await state.update_data({"company_name": message.text})
    await message.answer(f"Введите ваш Email")
    await state.set_state(FSMEmployerPoll.email)


@employer_pc_router.message(F.text, StateFilter(FSMEmployerPoll.email))
async def process_get_email(message: Message, state: FSMContext):
    await state.update_data({"email": message.text})
    await message.answer(f"Введите ваш номер телефона", reply_markup=kb_contact)
    await state.set_state(FSMEmployerPoll.phone)


@employer_pc_router.message(StateFilter(FSMEmployerPoll.phone), F.content_type.in_({ContentType.CONTACT}))
async def process_get_phone(message: Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await state.update_data({"tg_id": message.from_user.id})
    # TODO Произвести запись в базу даных
    tmp = await state.get_data()
    await message.answer(f"Тут производим запись кандидата в бд,\n"
                         f"{tmp}")
    # await db.insert_or_update_candidate()
    await message.answer(f"Спасибо что прошли опрос!\n"
                         f"Для дальнейшего размещения вакансий - "
                         f"отправьте свою геолокацию и отправьте боту форму",
                         reply_markup=kb_geo)
    await state.set_state(FSMEmployerPoll.geolocation)


@employer_pc_router.message(StateFilter(FSMEmployerPoll.geolocation), F.content_type.in_({ContentType.LOCATION}))
async def process_get_phone(message: Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await message.answer("Отправьте свою геолокацию", reply_markup=kb_geo)
    await state.set_state(FSMEmployerPoll.geolocation)
    tmp = await state.get_data()
    await message.answer(f"{tmp}")


# Этот хэндлер будет срабатывать на команду "/download_form"
# и отправлять в чат клавиатуру c url-кнопками
@employer_pc_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Форма для заполнения',
                         reply_markup=keyboard)


@employer_pc_router.message()
@employer_pc_router.callback_query()
async def process_start_command(message: Message):
    await message.answer("Вы что то делаете не так, перезапустите бот и попробуйте еще раз")
