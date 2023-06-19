from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Создаем кнопки
contact_btn: KeyboardButton = KeyboardButton(
    text='Отправить телефон',
    request_contact=True)

geo_btn: KeyboardButton = KeyboardButton(
    text='Отправить геолокацию',
    request_location=True)

# Инициализируем билдерp
kb_contact_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_geo_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер
kb_contact_builder.row(contact_btn, width=1)
kb_geo_builder.row(geo_btn, width=1)

# Создаем объект клавиатуры
kb_contact: ReplyKeyboardMarkup = kb_contact_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True)
kb_geo: ReplyKeyboardMarkup = kb_geo_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True)



# Создаем объекты инлайн-кнопок
url_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='Скачать файл',
    url='https://disk.yandex.ru/d/0_2sJJ3xGDKlfA')

# Создаем объект инлайн-клавиатуры
keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[url_button_1]])
