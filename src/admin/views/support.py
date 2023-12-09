from starlette_admin import fields

from src.admin.contrib.tortoise import ModelView, Admin
from src.admin import icons
from src.models.support import Mail


class MailView(ModelView):
    model = Mail
    identity = 'mails'

    fields = [
        fields.IntegerField('id'),
        fields.StringField('text'),
        fields.StringField('answer'),
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


def register(admin: Admin):
    admin.add_view(MailView(icon=icons.MAIL))
