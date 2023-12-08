from typing import Callable, Dict, Any, Awaitable, Union, List

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from src.services import profile as profile_service
from src.models.profile import Profile
from src.bot.keyboards.inline.auth import build_register_kb
from src.bot.misc import icons


class ProfileMiddleware(BaseMiddleware):
    kwargs_key = 'profile'
    required_profile_message = ' '.join([icons.warning, 'Для этого действия требуется регистрация'])

    def __init__(self, required: bool = False):
        self.required = required

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        profile: Profile = await profile_service.get_or_none_by_telegram_user_id(event.from_user.id)

        if profile is None and self.required:
            if isinstance(event, Message):
                return await event.answer(self.required_profile_message, reply_markup=build_register_kb())
            elif isinstance(event, CallbackQuery):
                return await event.answer(self.required_profile_message, show_alert=True)

        data[self.kwargs_key] = profile
        return await handler(event, data)
