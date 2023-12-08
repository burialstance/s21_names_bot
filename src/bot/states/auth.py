from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    set_s21_login = State()
    set_telegram_login = State()
