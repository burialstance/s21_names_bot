from aiogram.fsm.state import State, StatesGroup


class ProfileState(StatesGroup):
    set_s21_login = State()
    set_telegram_login = State()
