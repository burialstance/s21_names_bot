from src.config.settings import settings

from src.admin.contrib.tortoise import Admin
from src.admin import views


admin = Admin(title=settings.APP_TITLE)
views.register(admin)
