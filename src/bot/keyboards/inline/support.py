import enum
import textwrap
from typing import Optional, Any

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.misc import icons
from src.models.support import Mail


class SupportAction(str, enum.Enum):
    NEW_MESSAGE = 'new_message'
    ALL_MESSAGES = 'all_messages'
    BACK = 'back_to_support'


class SupportCallback(CallbackData, prefix='support'):
    action: SupportAction
    payload: Optional[Any] = None


class SupportMessageAction(str, enum.Enum):
    SEND_MESSAGE = 'send'
    MESSAGE_DETAIL = 'detail'


class SupportMessageCallback(CallbackData, prefix='support_messages'):
    action: SupportMessageAction
    payload: Optional[Any] = None


new_message_btn = InlineKeyboardButton(
    text=' '.join(filter(None, [icons.message, 'Написать'])),
    callback_data=SupportCallback(action=SupportAction.NEW_MESSAGE).pack()
)

back_to_support_btn = InlineKeyboardButton(
    text=' '.join(filter(None, ['Назад'])),
    callback_data=SupportCallback(action=SupportAction.BACK).pack()
)

support_message_send_btn = InlineKeyboardButton(
    text=' '.join(filter(None, ['Отправить'])),
    callback_data=SupportMessageCallback(action=SupportMessageAction.SEND_MESSAGE).pack()
)


def build_support_kb(have_unseen_messages: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(new_message_btn)

    kb.add(InlineKeyboardButton(
        text=' '.join(filter(None, [
            icons.mailbox_full if have_unseen_messages else icons.mailbox_empty,
            'Мои обращения'
        ])),
        callback_data=SupportCallback(action=SupportAction.ALL_MESSAGES).pack()
    ))
    return kb.adjust(1).as_markup()


def build_typing_message_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(back_to_support_btn)
    return kb.adjust(1).as_markup()


def build_send_message_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(support_message_send_btn)
    kb.add(back_to_support_btn)
    return kb.adjust(1).as_markup()


def build_message_detail_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(back_to_support_btn)
    return kb.adjust(1).as_markup()


def build_user_support_messages_kb(mails: list[Mail], offset: int = 0, limit: int = 0):
    kb = InlineKeyboardBuilder()

    for mail in mails:
        kb.add(InlineKeyboardButton(
            text=' '.join(filter(None, [
                icons.check if mail.answer else None,
                textwrap.shorten(mail.text, 16)
            ])),
            callback_data=SupportMessageCallback(
                action=SupportMessageAction.MESSAGE_DETAIL,
                payload=mail.id
            ).pack()
        ))

    kb.add(back_to_support_btn)
    return kb.adjust(1).as_markup()
