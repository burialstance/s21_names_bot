import enum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.misc import icons


class AuthAction(str, enum.Enum):
    REGISTER = 'register'
    REGISTER_FINISH = 'register_finish'


class AuthCallback(CallbackData, prefix='auth'):
    action: AuthAction


registration_btn = InlineKeyboardButton(
    text=' '.join(filter(None, [icons.new, 'Регистрация'])),
    callback_data=AuthCallback(action=AuthAction.REGISTER).pack()
)

finish_registration_btn = InlineKeyboardButton(
    text=' '.join(filter(None, [icons.thumbs_up, 'Да, все верно'])),
    callback_data=AuthCallback(action=AuthAction.REGISTER_FINISH).pack()
)


def build_register_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(registration_btn)
    return kb.adjust(1).as_markup()


def build_finish_register_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(finish_registration_btn)
    return kb.adjust(1).as_markup()
