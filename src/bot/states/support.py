from aiogram.fsm.state import State, StatesGroup


class SupportState(StatesGroup):
    message_typing = State()
