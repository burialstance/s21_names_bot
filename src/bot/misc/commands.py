import enum
from typing import List

from aiogram import Bot, types

from src.bot.misc import icons

START_CMD = 'start'
PROFILE_CMD = 'profile'
HELP_CMD = 'help'
DELETE_CMD = 'delete'
SUPPORT_CMD = 'support'

BOT_COMMANDS = {
    PROFILE_CMD: ' '.join(filter(None, [icons.person, 'Мой профиль'])),
    DELETE_CMD: ' '.join(filter(None, [icons.delete, 'Удалить мой профиль'])),
    SUPPORT_CMD: ' '.join(filter(None, [icons.message, 'Напиши нам'])),
    HELP_CMD: ' '.join(filter(None, ['Помочь?'])),
}


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(
        commands=[types.BotCommand(command=c, description=d) for c, d in BOT_COMMANDS.items()],
        scope=types.BotCommandScopeAllPrivateChats()
    )
