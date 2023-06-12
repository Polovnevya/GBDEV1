from aiogram import Bot, Dispatcher
import logging
from config.config import config

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Инициализируем базу данных
#db: DataBase = DataBase(config.db.database)

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token,
               parse_mode='HTML')
dp: Dispatcher = Dispatcher()

