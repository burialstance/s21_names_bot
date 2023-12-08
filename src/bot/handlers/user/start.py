from typing import Optional, Any

from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration

from src.bot.misc import icons
from src.bot.middlewares.profile import ProfileMiddleware
from src.bot.keyboards.inline.auth import build_register_kb
from src.models.profile import Profile

router = Router()
router.message.outer_middleware.register(ProfileMiddleware())


@router.message(CommandStart())
async def on_start(message: types.Message, profile: Optional[Profile], state: FSMContext):
    await state.clear()

    text = [
        'Привет! Я бот для поиска пользователей по школьному или телеграм нику.',
    ]
    reply_markup = None

    if profile is None:
        text.extend([
            'Для продолжения работы тебе придется зарегистрироваться',
        ])
        reply_markup = build_register_kb()
    else:
        text.extend([
            'Если у тебя возникли вопросы или проблемы - пиши /help'
        ])

    await message.answer('\n'.join(text), reply_markup=reply_markup)


