from aiogram.utils.text_decorations import html_decoration
from pydantic import ConfigDict

from src.models.profile import Profile
from .base import BasePage


class ProfilePage(BasePage):
    profile: Profile

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    @classmethod
    async def create(cls, profile: Profile):
        await profile.fetch_related('school_user', 'telegram_user')
        return ProfilePage(
            profile=profile,
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

    # def build_text(self, disable_decoration: bool = False) -> str:
    #     return '\n'.join([
    #         'Твой профиль(так его видят остальные)',
    #         '',
    #         self.build_public_text()
    #     ])

    def build_public_text(self) -> str:
        # rows = []
        # rows.append(' '.join([
        #     'school username:',
        #     html_decoration.link(self.profile.school_user.username, self.profile.school_user.profile_url)
        # ]))
        # rows.append(' '.join([
        #     'telegram username:',
        #     f'@{self.profile.telegram_user.username}'
        # ]))
        # return '\n'.join(rows)
        return self.build_text()
