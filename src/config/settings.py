from pathlib import Path

import humanize
from pydantic_settings import BaseSettings, SettingsConfigDict

humanize.i18n.activate("ru_RU")

_BASE_DIR = Path(__file__).parent.parent
_ENV_FILE = _BASE_DIR.parent.joinpath('.env')


class Settings(BaseSettings):
    BASE_DIR: Path = _BASE_DIR
    DEBUG: bool = True
    APP_TITLE: str = 's21_ournames bot'
    APP_VERSION: str = '0.0.1'

    TELEGRAM_BOT_TOKEN: str

    DATABASE_URI: str = f'sqlite://{BASE_DIR.parent}/db.sqlite'

    model_config = SettingsConfigDict(env_file=_ENV_FILE, extra='ignore')


settings = Settings()
