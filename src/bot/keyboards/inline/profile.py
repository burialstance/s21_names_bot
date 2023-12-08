import enum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder

from ...misc import icons


class ProfileAction(str, enum.Enum):
    SCHOOL_USERNAME_CHANGE = 'school_username_change'
    TELEGRAM_USERNAME_CHANGE = 'telegram_username_change'
    DELETE = 'delete'


class ProfileCallback(CallbackData, prefix='profile'):
    action: ProfileAction


school_username_change_btn = InlineKeyboardButton(
    text=' '.join([icons.school, 'Изменить школьный логин']),
    callback_data=ProfileCallback(action=ProfileAction.SCHOOL_USERNAME_CHANGE).pack()
)

telegram_username_change_btn = InlineKeyboardButton(
    text=' '.join([icons.phone, 'Изменить телеграм логин']),
    callback_data=ProfileCallback(action=ProfileAction.TELEGRAM_USERNAME_CHANGE).pack()
)

delete_profile_btn = InlineKeyboardButton(
    text=' '.join([icons.delete, 'Удалить профиль']),
    callback_data=ProfileCallback(action=ProfileAction.DELETE).pack()
)


def build_profile_private_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(school_username_change_btn)
    kb.add(telegram_username_change_btn)
    return kb.adjust(1).as_markup()


def build_delete_profile_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(delete_profile_btn)
    return kb.adjust(1).as_markup()
