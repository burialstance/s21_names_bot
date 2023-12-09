import enum
from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder

from ...misc import icons


class ProfileAction(str, enum.Enum):
    SCHOOL_USERNAME_CHANGE = 'school_username_change'
    TELEGRAM_USERNAME_CHANGE = 'telegram_username_change'
    SET_TELEGRAM_USERNAME = 'set_telegram_username'

    DELETE = 'delete'
    APPROVE_DELETE = 'approve_delete'

    BACK_TO_PROFILE = 'back_to_profile'


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

approve_delete_profile_btn = InlineKeyboardButton(
    text=' '.join([icons.approve_delete, 'Да, я уверен']),
    callback_data=ProfileCallback(action=ProfileAction.APPROVE_DELETE).pack()
)

back_to_profile_btn = InlineKeyboardButton(
    text=' '.join([icons.back, 'Назад']),
    callback_data=ProfileCallback(action=ProfileAction.BACK_TO_PROFILE).pack()
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


def build_approve_delete_profile_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(approve_delete_profile_btn)
    return kb.adjust(1).as_markup()


def build_setup_school_login_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(back_to_profile_btn)
    return kb.adjust(1).as_markup()


def build_setup_telegram_login_kb(default_username: Optional[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if default_username is not None:
        kb.add(InlineKeyboardButton(
            text=default_username,
            callback_data=ProfileCallback(action=ProfileAction.SET_TELEGRAM_USERNAME).pack()
        ))

    kb.add(back_to_profile_btn)
    return kb.adjust(1).as_markup()
