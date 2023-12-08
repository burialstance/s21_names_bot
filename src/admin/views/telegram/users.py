from starlette_admin import fields
from starlette.requests import Request

from src.admin.contrib.tortoise import ModelView
from src.models.telegram import TelegramUser


class TelegramUserView(ModelView):
    model = TelegramUser
    identity = 'telegram_users'

    fields = [
        fields.IntegerField('id'),
        fields.StringField('username'),
        fields.HasOne('profile', identity='profiles'),
        fields.StringField('created_at_humanize'),
        fields.StringField('updated_at_humanize'),
    ]

    exclude_fields_from_create = [
        'created_at_humanize',
        'updated_at_humanize'
    ]
    exclude_fields_from_edit = exclude_fields_from_create

    def get_queryset(self):
        return self.model.all().prefetch_related('profile')

    async def repr(self, obj: TelegramUser, request: Request) -> str:
        return obj.username
