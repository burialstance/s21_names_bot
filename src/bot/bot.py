from aiogram import Dispatcher, Bot

from src.config.settings import settings

from src.bot import handlers
from src.bot.misc import commands

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode='HTML')

dp = Dispatcher()
handlers.register(dp)


@dp.startup()
async def on_startup():
    await commands.set_bot_commands(bot)
    print('bot on_startup')


@dp.shutdown()
async def on_shutdown():
    print('bot on_shutdown')
