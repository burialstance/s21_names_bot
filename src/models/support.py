import textwrap
from typing import Optional

from pydantic import BaseModel
from tortoise import fields

from src.db import mixins


class Mail(mixins.Timestamped, mixins.Model):
    profile: fields.ForeignKeyNullableRelation['Profile'] = fields.ForeignKeyField(
        'models.Profile', 'mails', fields.SET_NULL, null=True
    )

    text: str = fields.TextField()
    answer: Optional[str] = fields.TextField(null=True)

    @property
    def text_short(self, max_length: int = 64):
        return textwrap.shorten(self.text, max_length)

    @property
    def answer_short(self, max_length: int = 64):
        return textwrap.shorten(self.answer, max_length)


class MailCreate(BaseModel):
    profile_id: int
    text: str
