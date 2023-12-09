from typing import Optional, List

from tortoise import BaseDBAsyncClient
from tortoise.exceptions import DoesNotExist
from tortoise.signals import post_save

from src.bot.pages.support import SupportMailAdminPage
from src.models.telegram.user import TelegramUser
from src.models.profile import Profile

from src.models.support import Mail, MailCreate


@post_save(Mail)
async def on_mail_save(
        sender: "Type[Mail]",
        instance: Mail,
        created: bool,
        using_db: Optional[BaseDBAsyncClient],
        update_fields: List[str],
) -> None:
    if created:
        await notify_admins_new_mail(instance)
    else:
        print('mail saved')


async def create_mail(mail_in: MailCreate) -> Mail:
    return await Mail.create(**mail_in.model_dump())


async def notify_admins_new_mail(mail: Mail):
    from src.bot.main import bot  # broken circular imports
    from src.services.telegram import user as telegram_user_service

    admins: List[TelegramUser] = await telegram_user_service.get_admins()
    if not admins:
        print('no admin exist, skip mail notify')
        return

    mail_page = await SupportMailAdminPage.create(mail)
    for admin in admins:
        await bot.send_message(
            chat_id=admin.id,
            text=mail_page.build_text(),
            # reply_markup=... todo kb to interact with mails
        )


async def get_by_id(id: int) -> Mail:
    return await Mail.get(id=id)


async def get_or_none_by_id(id: int) -> Optional[Mail]:
    try:
        return await get_by_id(id)
    except DoesNotExist:
        ...
