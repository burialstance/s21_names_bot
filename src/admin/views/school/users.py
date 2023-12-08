from starlette.requests import Request
from starlette_admin import fields
from src.admin.contrib.tortoise import ModelView
from src.models.school import SchoolUser


class SchoolUserView(ModelView):
    model = SchoolUser
    identity = 'school_users'

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

    async def repr(self, obj: SchoolUser, request: Request) -> str:
        return obj.username
