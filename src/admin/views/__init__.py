from src.admin.contrib.tortoise import Admin

from . import profiles
from . import school
from . import telegram


def register(admin: Admin):
    profiles.register(admin)

    school.register(admin)
    telegram.register(admin)
