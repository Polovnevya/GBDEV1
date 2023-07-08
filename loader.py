from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import utils.appsched
from config.config import config
from db.sql_facade import DAO, SqlManager

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Инициализируем базу данных
db: DAO = DAO(SqlManager(config))

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token,
               parse_mode='HTML')
dp: Dispatcher = Dispatcher()

# Инициализируем шедулер
scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone="Europe/Moscow")
scheduler.add_job(utils.appsched.auto_posting,
                  trigger='interval',
                  seconds=120,
                  kwargs={'bot': bot,
                          'db': db})

