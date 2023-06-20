import os
import pandas as pd
from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter, CommandStart, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
# from db.models import GenderEnum, AgeCategoriesEnum, EducationEnum
from keyboards.candidate import kb_contact, kb_geo
from keyboards.employer import customer_action_1, customer_action_2
from keyboards.inline.employer import get_personal_data_keyboard, PersonalData
from keyboards.inline.candidate import EducationCallback
from loader import db
from states.employer import FSMEmployerPoll
from keyboards.employer import keyboard_employer_start, keyboard_url_button


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
async def process_button_1_press(callback: CallbackQuery):
    await callback.message.answer(
        text=f'Скачайте, заполните и направьте форму в бот для размещения вакансии\n')
    await callback.message.answer(text='Скачать форму для заполнения',
                                  reply_markup=keyboard_url_button)

@employer_pc_router.message()
@employer_pc_router.callback_query()
async def process_start_command(message: Message):
    await message.answer("Вы что то делаете не так, перезапустите бот и попробуйте еще раз")
