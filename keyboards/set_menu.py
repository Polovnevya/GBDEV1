from aiogram import Bot
from aiogram.types import BotCommand


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(command="/bot", description="Запустить бота"),
                          ]
    await bot.set_my_commands(main_menu_commands)
