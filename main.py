import asyncio
import logging
import handlers
from db.fixtures import fixtures
from keyboards.set_main_menu import set_main_menu
from loader import dp, logger, bot, db, scheduler


# Функция конфигурирования и запуска бота
async def main():
    # Создает таблицы в бд
    await db.delete_db_tables(is_delete=False)
    await db.create_db_tables()
    await db.load_fixtures(fixtures)

    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(handlers.candidate.personal_cabinet.candidate_pc_router)
    dp.include_router(handlers.employer.personal_cabinet.employer_pc_router)

    dp.include_router(handlers.common.echo.router)

    scheduler.start()
    print(scheduler.print_jobs())

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
