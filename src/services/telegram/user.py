import asyncio
from typing import Optional, Tuple, List

from aiocache import cached, caches, SimpleMemoryCache
from tortoise.exceptions import DoesNotExist

from src.models.telegram import (
    TelegramUser,
    TelegramUserCreate
)


# CACHE_ALIAS = 'telegram_users'
# caches.add(CACHE_ALIAS, {
#     'ttl': 300,
#     'cache': 'aiocache.SimpleMemoryCache',
#     'serializer': {
#         'class': 'aiocache.serializers.NullSerializer'
#     }
# })
# cache = caches.get(CACHE_ALIAS)
# def get_cache_detail() -> dict:
#     assert isinstance(cache, SimpleMemoryCache), 'this available only on SimpleMemoryCache'
#     items = []
#     loop_time = asyncio.get_running_loop().time()
#     for cache_key in cache._cache.keys():
#         item = {'key': cache_key}
#         if handler := cache._handlers.get(cache_key):
#             item.update({'ttl': round(handler.when() - loop_time, 2)})
#         items.append(item)
#     return {
#         'ttl': cache.ttl,
#         'total': len(items),
#         'items': items
#     }

def get_cache_detail(cache: SimpleMemoryCache) -> dict:
    assert isinstance(cache, SimpleMemoryCache), 'this available only on SimpleMemoryCache'
    items = []
    loop_time = asyncio.get_running_loop().time()
    for cache_key in cache._cache.keys():
        item = {'key': cache_key}
        if handler := cache._handlers.get(cache_key):
            item.update({'ttl': round(handler.when() - loop_time, 2)})
        items.append(item)
    return {
        'ttl': cache.ttl,
        'total': len(items),
        'items': items
    }


# # @cached(alias=CACHE_ALIAS, key_builder=lambda f, *args, **kwargs: kwargs.get('user_id'))
# @cached(ttl=300, key_builder=lambda f, *args, **kwargs: kwargs.get('id'))
# async def get_or_none_by_id(*, id: int, session: AsyncSession) -> Optional[TelegramUser]:
#     return await session.scalar(
#         select(TelegramUser).where(TelegramUser.id == id)
#     )
#
#
# async def get_or_none_by_username(*, username: str, session: AsyncSession) -> Optional[TelegramUser]:
#     return await session.scalar(
#         select(TelegramUser).where(TelegramUser.username == username)
#     )
#
#
# async def create(*, user_in: TelegramUserCreate, session: AsyncSession) -> TelegramUser:
#     instance = TelegramUser(**user_in.model_dump())
#     session.add(instance)
#     await session.commit()
#
#     await session.refresh(instance)
#     return instance
#
#
# async def get_or_create(*, user_in: TelegramUserCreate, session: AsyncSession) -> Tuple[TelegramUser, bool]:
#     if user := await get_or_none_by_username(username=user_in.username, session=session):
#         return user, False
#     return await create(user_in=user_in, session=session), True

async def get_by_username(username: str) -> TelegramUser:
    return await TelegramUser.get(username=username)


async def get_or_none_by_username(username: str) -> Optional[TelegramUser]:
    try:
        return await get_by_username(username)
    except DoesNotExist:
        return None


async def create(user_in: TelegramUserCreate) -> TelegramUser:
    return await TelegramUser.create(**user_in.model_dump())


async def get_or_create(user_in: TelegramUserCreate) -> Tuple[TelegramUser, bool]:
    try:
        return await get_by_username(user_in.username), False
    except DoesNotExist:
        return await create(user_in), True


async def set_username(user: TelegramUser, username: str) -> TelegramUser:
    await user.update_from_dict({'username': username}).save()
    return user


async def get_admins() -> List[TelegramUser]:
    return await TelegramUser.all().filter(is_superuser=True)
