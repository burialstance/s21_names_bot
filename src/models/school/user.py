import datetime

from tortoise import fields

from pydantic import BaseModel, Field, field_validator

from src.db import mixins

import re
from typing import Optional
from email_validator import validate_email, ValidatedEmail, EmailSyntaxError


def extract_email_local_part(text: str) -> Optional[str]:
    """
    :param text: tyberora@student.21-school.ru
    :return: tyberora
    """
    try:
        validated: ValidatedEmail = validate_email(text)
        return validated.local_part
    except EmailSyntaxError:
        pass


def validate_s21_login(text: str) -> Optional[str]:
    text = extract_email_local_part(text) if '@' in text else text
    if text and (match := re.search(r'^[a-zA-Z0-9]{4,}$', text)):
        login = match.group()
        return login.lower()


class SchoolUser(mixins.Timestamped, mixins.Model):
    username: str = fields.CharField(255, unique=True)

    profile: fields.OneToOneRelation['Profile']

    @property
    def profile_url(self) -> str:
        return 'https://edu.21-school.ru/profile/{}@student.21-school.ru'.format(self.username)

    class Meta:
        table = 'school_user'


class SchoolUserBase(BaseModel):
    username: str

    @property
    def profile_url(self) -> str:
        return 'https://edu.21-school.ru/profile/{}@student.21-school.ru'.format(self.username)


class SchoolUserCreate(SchoolUserBase):
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str):
        if username := validate_s21_login(v):
            return username
        raise ValueError('incomplete username')


class SchoolUserRetrieve(SchoolUserBase):
    id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    profile_url: str
