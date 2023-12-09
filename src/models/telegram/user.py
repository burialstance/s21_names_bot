import datetime
from typing import Optional

from tortoise import fields

from pydantic import BaseModel, field_validator

from src.db import mixins


class TelegramUser(mixins.Timestamped, mixins.Model):
    username: str = fields.CharField(64, unique=True)
    is_superuser: bool = fields.BooleanField(default=False)

    profile: fields.OneToOneRelation['Profile']

    class Meta:
        table = 'telegram_user'


class TelegramUserBase(BaseModel):
    id: int
    username: str


class TelegramUserCreate(TelegramUserBase):

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str):
        return v


class TelegramUserRetrieve(TelegramUserBase):
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    is_superuser: bool
