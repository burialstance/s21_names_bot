from typing import Optional, Tuple

from tortoise.exceptions import DoesNotExist

from src.models.school import SchoolUser, SchoolUserCreate


async def get_by_username(username: str) -> SchoolUser:
    return await SchoolUser.get(username=username)


async def get_or_none_by_username(username: str) -> Optional[SchoolUser]:
    try:
        return await get_by_username(username)
    except DoesNotExist:
        return None


async def create(user_in: SchoolUserCreate) -> SchoolUser:
    return await SchoolUser.create(**user_in.model_dump())


async def get_or_create(user_in: SchoolUserCreate) -> Tuple[SchoolUser, bool]:
    try:
        return await get_by_username(user_in.username), False
    except DoesNotExist:
        return await create(user_in), True


async def set_username(user: SchoolUser, username: str) -> SchoolUser:
    await user.update_from_dict({'username': username}).save()
    return user
