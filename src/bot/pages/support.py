from typing import Optional

from src.bot.misc import icons
from src.models.profile import Profile
from src.services import profile as profile_service
from .base import BasePage
from ...models.support import Mail


class SupportMailPage(BasePage):
    icon: Optional[str] = icons.message

    @classmethod
    async def create(cls, profile: Profile):
        total_count = await profile_service.get_total_support_messages_count(profile)
        unseen_count = await profile_service.get_total_support_messages_count(profile, unseen_only=True)
        return cls(
            title='Мои обращения',
            content='\n'.join([
                f'Всего сообщений {total_count}',
                f'В обработке: {unseen_count}'
            ])
        )


class SupportMailDetailPage(BasePage):
    @classmethod
    async def create(cls, mail: Mail):
        desc = ' '.join(['Без ответа:', icons.sad_face])
        if mail.answer:
            desc = ' '.join(['Ответ:', mail.answer])

        return cls(
            icon=icons.message,
            title='Сообщение',
            content='"{}"'.format(mail.text),
            desc=desc
        )


class SupportMailAdminPage(BasePage):
    @classmethod
    async def create(cls, mail: Mail):
        return cls(
            icon=icons.message,
            title='New support mail',
            content=mail.text
        )
