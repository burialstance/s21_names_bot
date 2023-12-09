import random
from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from src.bot.misc import commands

router = Router()


@router.message(Command(commands=[commands.HELP_CMD]))
async def on_help(message: types.Message):
    text = random.choice([
        'Видишь эта крутится? - крути эту, что не крутится - не крути',
        'Преисполнись и все станет просто'
    ])
    await message.answer(text=text)
