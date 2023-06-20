from aiogram.filters.state import State, StatesGroup


class FSMEmployerPoll(StatesGroup):
    company_name = State()
    email = State()
    phone = State()
    geolocation = State()
    load_pd = State()


class FSMFormEvent(StatesGroup):
    lreporting = State()
