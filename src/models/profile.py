import datetime
from typing import Optional

from tortoise import fields

from pydantic import BaseModel

from src.db import mixins
from src.models.telegram import TelegramUserCreate, TelegramUserRetrieve
from src.models.school import SchoolUserCreate, SchoolUser, SchoolUserRetrieve


class Profile(mixins.Timestamped, mixins.Model):
    telegram_user: fields.OneToOneRelation['TelegramUser'] = fields.OneToOneField(
        'models.TelegramUser', 'profile', fields.CASCADE
    )
    school_user: fields.OneToOneRelation['SchoolUser'] = fields.OneToOneField(
        'models.SchoolUser', 'profile', fields.CASCADE
    )

    class Meta:
        table = 'profile'


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
