from aiogram.filters.state import State, StatesGroup


class FSMCandidatePoll(StatesGroup):
    first_name = State()
    middle_name = State()
    last_name = State()
    gender = State()
    age = State()
    education = State()
