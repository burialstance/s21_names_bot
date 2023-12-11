from typing import Optional, List

from tortoise import BaseDBAsyncClient
from tortoise.exceptions import DoesNotExist
from tortoise.signals import post_save

from src.bot.keyboards.inline.support import build_admin_support_mail_detail
from src.bot.misc import icons
from src.bot.pages.base import BasePage
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
    elif instance.answer:
        await notify_user_about_support_answer(instance)


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
            reply_markup=build_admin_support_mail_detail(mail_id=mail.id)
        )


async def get_by_id(id: int) -> Mail:
    return await Mail.get(id=id)


async def get_or_none_by_id(id: int) -> Optional[Mail]:
    try:
        return await get_by_id(id)
    except DoesNotExist:
        ...


async def create_answer_to_mail(mail: Mail, answer: str) -> Mail:
    await mail.update_from_dict({'answer': answer}).save(update_fields=['answer'])
    return mail


async def notify_user_about_support_answer(mail: Mail):
    from src.bot.main import bot

    await mail.fetch_related('profile')
    if mail.profile is None:
        return

    await bot.send_message(
        chat_id=mail.profile.telegram_user_id,
        text=BasePage(
            icon=icons.message_heart,
            title='Получен ответ на обращение',
            desc='Посмотреть во вкладке "Мои сообщения" /support'
        ).build_text()
    )