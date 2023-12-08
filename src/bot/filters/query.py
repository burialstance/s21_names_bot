from aiogram import types, filters


class QueryFilter(filters.Filter):
    async def __call__(self, message: types.Message) -> bool:
        if text := message.text:
            return all([
                '/' not in text,
                all([not i.isspace() and i.isascii() for i in text]),
            ])
