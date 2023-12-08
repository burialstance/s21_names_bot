from aiogram.utils.text_decorations import html_decoration
from pydantic import BaseModel, ConfigDict

from src.models.profile import Profile


class ProfilePage(BaseModel):
    profile: Profile

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    @classmethod
    async def create(cls, profile: Profile):
        await profile.fetch_related('school_user', 'telegram_user')
        return ProfilePage(profile=profile)

    def build_text(self) -> str:
        return '\n'.join([
            'Твой профиль(так его видят остальные)',
            '',
            self.build_public_text()
        ])

    def build_public_text(self) -> str:
        rows = []

        rows.append(' '.join([
            'school username:',
            html_decoration.link(self.profile.school_user.username, self.profile.school_user.profile_url)
        ]))
        rows.append(' '.join([
            'telegram username:',
            f'@{self.profile.telegram_user.username}'
        ]))
        return '\n'.join(rows)
