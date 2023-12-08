from aiogram import types, filters, F
from aiogram import Router

from src.bot.filters.query import QueryFilter
from src.bot.middlewares.profile import ProfileMiddleware
from src.bot.misc import icons

from src.services import profile as profile_service

from src.bot.pages.profile import ProfilePage

router = Router()
router.message.outer_middleware.register(ProfileMiddleware(required=True))


@router.message(QueryFilter())
async def on_query(message: types.Message):
    if profile := await profile_service.search_profile(message.text):
        profile_page = await ProfilePage.create(profile)
        await message.answer(profile_page.build_public_text())
    else:
        await message.answer(' '.join([icons.dont_know, 'Ничего не нашел']))
