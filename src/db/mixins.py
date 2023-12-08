import datetime
import re
from typing import Optional

from tortoise import fields, Model as TortoiseModel
import humanize


class Timestamped(object):
    created_at: datetime.datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime.datetime = fields.DatetimeField(auto_now=True)

    @property
    def created_at_humanize(self) -> str:
        return humanize.naturaldate(self.created_at)

    @property
    def updated_at_humanize(self) -> Optional[str]:
        if self.updated_at:
            return humanize.naturaldelta(self.created_at - self.updated_at)


class Model(TortoiseModel):
    id: int = fields.BigIntField(pk=True, index=True)

    class Meta:
        abstract = True
