from typing import Optional

from pydantic import BaseModel, Field
from aiogram.utils.text_decorations import html_decoration


class BasePage(BaseModel):
    title: str
    icon: Optional[str] = Field(None)
    content: Optional[str] = Field(None)
    desc: Optional[str] = Field(None)

    def build_text(self, disable_decoration: bool = False) -> str:
        rows = [self._build_header(disable_decoration)]

        if self.content:
            rows.append('')
            rows.append(self.content)

        if self.desc:
            rows.append('')
            rows.append(self.desc if disable_decoration else html_decoration.italic(self.desc))

        return '\n'.join(rows)

    def _build_header(self, disable_decoration: bool = False) -> str:
        return ' '.join(filter(None, [
            self.icon,
            self.title if disable_decoration else html_decoration.bold(self.title)
        ]))
