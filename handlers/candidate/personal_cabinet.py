from aiogram import Router, F
from aiogram.types import Message

from db.models import GenderEnum
from keyboards.inline.candidate import get_gender_keyboard_fab

candidate_pc_router: Router = Router()



@candidate_pc_router.message(F.text)
async def process_start_command(message: Message):
    await message.answer(message.text,
                         reply_markup=get_gender_keyboard_fab(GenderEnum))
    a = 1 + 7
