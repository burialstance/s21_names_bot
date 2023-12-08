import random
from aiogram import Router, types
from aiogram.filters import CommandStart, Command


router = Router()


@router.message(Command(commands=['help']))
async def on_help(message: types.Message):
    text = random.choice([
        'Видишь эта крутится? - крути эту, что не крутится - не крути',
        'Напиши ченить - не укушу'
    ])
    await message.answer(text=text)
