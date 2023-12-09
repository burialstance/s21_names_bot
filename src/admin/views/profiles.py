from starlette_admin import fields

from src.admin.contrib.tortoise import ModelView, Admin
from src.admin import icons
from src.models.profile import Profile


class ProfileView(ModelView):
    model = Profile
    identity = 'profiles'

    fields = [
        fields.IntegerField('id'),
        fields.HasOne('telegram_user', identity='telegram_users'),
        fields.HasOne('school_user', identity='school_users'),
        fields.StringField('created_at_humanize'),
        fields.StringField('updated_at_humanize'),
        fields.StringField('last_activity_humanize'),
    ]

    exclude_fields_from_create = [
        'created_at_humanize',
        'updated_at_humanize'
    ]
    exclude_fields_from_edit = exclude_fields_from_create

    def get_queryset(self):
        return self.model.all().prefetch_related('telegram_user', 'school_user')


def register(admin: Admin):
    admin.add_view(ProfileView(icon=icons.CARD))
