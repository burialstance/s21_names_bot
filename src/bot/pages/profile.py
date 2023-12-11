from aiogram.utils.text_decorations import html_decoration
from pydantic import ConfigDict

from src.models.profile import Profile
from .base import BasePage
from ..misc import icons


class ProfilePage(BasePage):
    @classmethod
    async def create(cls, profile: Profile):
        await profile.fetch_related('school_user', 'telegram_user')
        return ProfilePage(
            icon=icons.person,
            title='Профиль пользователя',
            content='\n'.join([
                ' '.join([
                    html_decoration.bold('school username:'),
                    html_decoration.link(profile.school_user.username, profile.school_user.profile_url)
                ]),
                ' '.join([
                    html_decoration.bold('telegram username:'),
                    f'@{profile.telegram_user.username}'
                ])
            ]),
            desc=' '.join([
                'Последняя активность',
                profile.last_activity_humanize,
            ])
        )
