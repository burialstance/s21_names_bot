from aiogram.fsm.state import State, StatesGroup


class SupportState(StatesGroup):
    message_typing = State()


class SupportAdminState(SupportState):
    answer_typing = State()
