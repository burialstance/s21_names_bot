import datetime
from typing import Optional

import humanize
from tortoise import fields
from tortoise.timezone import now

from pydantic import BaseModel

from src.db import mixins
from src.models.telegram import TelegramUserCreate, TelegramUserRetrieve
from src.models.school import SchoolUserCreate, SchoolUser, SchoolUserRetrieve


class Profile(mixins.Timestamped, mixins.Model):
    last_activity: datetime.datetime = fields.DatetimeField(auto_now_add=True)

    telegram_user: fields.OneToOneRelation['TelegramUser'] = fields.OneToOneField(
        'models.TelegramUser', 'profile', fields.CASCADE
    )
    school_user: fields.OneToOneRelation['SchoolUser'] = fields.OneToOneField(
        'models.SchoolUser', 'profile', fields.CASCADE
    )

    mails: fields.ReverseRelation['Mail']

    class Meta:
        table = 'profile'

    @property
    def last_activity_humanize(self) -> str:
        return humanize.naturaldelta(now() - self.last_activity)


class ProfileCreate(BaseModel):
    telegram_user: TelegramUserCreate
    school_user: SchoolUserCreate


class ProfileRetrieve(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    telegram_user_id: int
    school_user_id: int


class ProfileRetrieveDetail(BaseModel):
    telegram_user: TelegramUserRetrieve
    school_user: SchoolUserRetrieve
