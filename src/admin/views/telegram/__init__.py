from starlette_admin.views import DropDown

from src.models.telegram import TelegramUser
from src.admin import icons
from src.admin.contrib.tortoise import Admin

from . import users


def register(admin: Admin):
    admin.add_view(DropDown('Telegram', icon=icons.USERS, views=[
        users.TelegramUserView(TelegramUser)
    ]))
