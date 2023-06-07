from aiogram import Router, F
from aiogram.types import Message

router: Router = Router()


# Этот хэндлер будет срабатывать на любой текст
@router.message(F.text)
async def process_start_command(message: Message):
    await message.answer(message.text)
