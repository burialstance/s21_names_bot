from typing import Callable, Dict, Any, Awaitable, Union, List

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from src.bot.pages.error import ErrorPage
from src.services import profile as profile_service
from src.models.profile import Profile
from src.bot.keyboards.inline.auth import build_register_kb


class ProfileMiddleware(BaseMiddleware):
    kwargs_key = 'profile'
    required_profile_text = 'Для этого действия требуется регистрация'

    def __init__(self, required: bool = False):
        self.required = required

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        profile: Profile
        data[self.kwargs_key] = profile = await profile_service.get_or_none_by_telegram_user_id(event.from_user.id)

        if profile:
            await profile_service.set_activity(profile)

        if profile is None and self.required:
            if isinstance(event, Message):
                return await event.answer(
                    ErrorPage(title=self.required_profile_text).build_text(),
                    reply_markup=build_register_kb()
                )
            elif isinstance(event, CallbackQuery):
                return await event.answer(
                    ErrorPage(title=self.required_profile_text).build_text(disable_decoration=True),
                    show_alert=True
                )
        return await handler(event, data)
