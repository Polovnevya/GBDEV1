from aiogram import Bot, Dispatcher
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.config import config
from db.sql_facade import DAO, SqlManager

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Инициализируем базу данных
db: DAO = DAO(SqlManager(config))

# Инициализируем шедулер
scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone="Europe/Moscow")

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token,
               parse_mode='HTML')
dp: Dispatcher = Dispatcher()
