from src.admin.contrib.tortoise import Admin

from . import profiles
from . import school
from . import telegram
from . import support


def register(admin: Admin):
    profiles.register(admin)
    support.register(admin)
    school.register(admin)
    telegram.register(admin)
