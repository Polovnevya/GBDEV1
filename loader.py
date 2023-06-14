from aiogram import Bot, Dispatcher
import logging
from config.config import config
from db.sql_facade import SqlHelper, SqlManager

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Инициализируем базу данных
db: SqlHelper = SqlHelper(config, SqlManager)

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token,
               parse_mode='HTML')
dp: Dispatcher = Dispatcher()

