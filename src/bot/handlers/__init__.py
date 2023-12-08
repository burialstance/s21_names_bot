from aiogram import Dispatcher, Router

from . import user

root_router = Router()

root_router.include_router(user.router)


def register(dp: Dispatcher):
    dp.include_router(root_router)
