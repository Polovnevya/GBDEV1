from aiogram import types

button_phone = types.KeyboardButton(text="Отправить контакт", request_contact=True)
keyboard_phone = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard_phone.add(button_phone)

button_geo = types.KeyboardButton(text="Отправить геолокацию", request_location=True)
keyboard_geo = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard_geo.add(button_phone)