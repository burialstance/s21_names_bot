from aiogram import Bot, types

from src.bot.misc import icons

START_CMD = 'start'
PROFILE_CMD = 'profile'
HELP_CMD = 'help'
DELETE_CMD = 'delete'

BOT_COMMANDS = {
    PROFILE_CMD: ' '.join(filter(None, ['Show your profile'])),
    START_CMD: ' '.join(filter(None, ['Show start message'])),
    HELP_CMD: ' '.join(filter(None, ['Show help message'])),

    DELETE_CMD: ' '.join(filter(None, [icons.delete, 'Delete my accounts'])),
}


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(
        commands=[types.BotCommand(command=c, description=d) for c, d in BOT_COMMANDS.items()],
        scope=types.BotCommandScopeAllPrivateChats()
    )
