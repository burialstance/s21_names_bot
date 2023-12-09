from typing import Optional

from tortoise.expressions import Q
from tortoise.timezone import now
from tortoise.transactions import in_transaction

# from tortoise import Q

from src.models.profile import Profile, ProfileCreate


async def search_profile(q: str) -> Optional[Profile]:
    q = q.lower()
    return await Profile.all().filter(
        Q(telegram_user__username__iexact=q) | Q(school_user__username__iexact=q)
    ).first()


async def create(profile_in: ProfileCreate) -> Profile:
    from src.services.school import user as school_user_service
    from src.services.telegram import user as telegram_user_service

    school_user, _ = await school_user_service.get_or_create(profile_in.school_user)
    telegram_user, _ = await telegram_user_service.get_or_create(profile_in.telegram_user)

    return await Profile.create(school_user=school_user, telegram_user=telegram_user)


async def get_or_none_by_telegram_user_id(id: int) -> Optional[Profile]:
    return await Profile.get_or_none(telegram_user_id=id)


async def get_or_none_by_school_username(username: str) -> Optional[Profile]:
    return await Profile.get_or_none(school_user__username__iexact=username)


async def delete_cascade(profile: Profile) -> bool:
    await profile.fetch_related('telegram_user', 'school_user')
    async with in_transaction() as connection:
        await profile.telegram_user.delete(using_db=connection)
        await profile.school_user.delete(using_db=connection)
        await profile.delete(using_db=connection)
        return True


async def set_activity(profile: Profile) -> Profile:
    await profile.update_from_dict({'last_activity': now()}).save()
    return profile
