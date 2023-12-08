from fastapi import FastAPI

from src.config.logs import configure_logging
from src.config.settings import settings

from src.db import register_database
from src.bot import register_bot_app
from src.admin import register_admin_app
# from src.api import register_api_routes

configure_logging(20)

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
)

# register_api_routes(app)
register_database(app, generate_schemas=True, drop_databases=False)
register_bot_app(app)
register_admin_app(app)
