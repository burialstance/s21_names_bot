from starlette_admin.views import DropDown

from src.models.school import SchoolUser
from src.admin import icons
from src.admin.contrib.tortoise import Admin

from . import users


def register(admin: Admin):
    admin.add_view(DropDown('School 21', icon=icons.USERS, views=[
        users.SchoolUserView(SchoolUser)
    ]))
