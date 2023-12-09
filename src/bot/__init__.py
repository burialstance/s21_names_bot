import asyncio

from fastapi import FastAPI

from .main import dp, bot


def register_bot_app(app: FastAPI):
    @app.on_event('startup')
    async def on_startup():
        app.state.bot_pooling_task = asyncio.create_task(
            dp.start_polling(bot, handle_signals=False)
        )

    @app.on_event('shutdown')
    async def on_shutdown():
        # await dp.stop_polling()
        app.state.bot_pooling_task.cancel()
