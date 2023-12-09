from typing import Optional

from src.bot.misc import icons

from .base import BasePage


class ErrorPage(BasePage):
    icon: Optional[str] = icons.warning
