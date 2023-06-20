from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsEmployer(BaseFilter):
    def __init__(self, employers_id: List[int]) -> None:
        self.employers_id = employers_id

    async def __call__(self, m: Message) -> bool:
        return m.from_user.id in self.employers_id
