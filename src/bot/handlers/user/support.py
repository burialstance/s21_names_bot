from typing import Optional, Any

from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration

from src.bot.misc import icons, commands
from src.bot.pages.error import ErrorPage
from src.bot.pages.support import SupportMailPage, SupportMailDetailPage
from src.bot.states.support import SupportState, SupportAdminState
from src.bot.middlewares.profile import ProfileMiddleware
from src.bot.pages.base import BasePage
from src.models.profile import Profile
from src.bot.keyboards.inline.support import (
    build_user_support_kb,
    build_user_typing_message_kb,
    build_user_send_message_kb,
    build_user_support_messages_kb,
    build_message_detail_kb,
    SupportCallback,
    SupportAction,
    SupportMessageAction,
    SupportMessageCallback,
    SupportAdminCallback,
    SupportAdminAction, build_admin_support_type_answer_kb
)
from src.models.support import MailCreate
from src.services import support as support_service
from src.services import profile as profile_service

router = Router()

_profile_middleware = ProfileMiddleware(required=True)
router.message.outer_middleware.register(_profile_middleware)
router.callback_query.outer_middleware.register(_profile_middleware)


async def show_support_page(message: types.Message, edit: bool = False):
    text = BasePage(
        title='Поддержка',
        content='Тут мы будем обмениваться лестью или какашками',
        desc='\n'.join([
            f'>> {message.from_user.username or "anonym"}: ты пидр',
            f'>> Поддержка: сам ты пидр {icons.angry_face}',
        ])
    ).build_text()
    reply_markup = build_user_support_kb()

    if edit:
        await message.edit_text(text, reply_markup=reply_markup)
    else:
        await message.answer(text, reply_markup=reply_markup)


@router.message(Command(commands=[commands.SUPPORT_CMD]))
async def on_support(message: types.Message):
    await show_support_page(message, edit=False)


@router.callback_query(SupportCallback.filter(F.action == SupportAction.NEW_MESSAGE))
async def process_support_new_message(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SupportState.message_typing)
    await callback.message.edit_text(
        BasePage(
            title='Написать в поддержку',
            content='Отправь текст - а мы отправим ответ (:',
            desc='p.s а может и не отправим)))'
        ).build_text(),
        reply_markup=build_user_typing_message_kb()
    )


@router.message(StateFilter(SupportState.message_typing))
async def process_support_new_mail(message: types.Message, state: FSMContext, profile: Profile):
    if len(message.text) < 2:
        return await message.answer(
            BasePage(title='Слишком коротко', content='или буквы платные?').build_text(),
            reply_markup=build_user_typing_message_kb()
        )

    try:
        mail = MailCreate(text=message.text, profile_id=profile.id)
    except ValueError:
        await state.clear()
        await message.answer(ErrorPage(
            title='Что-то пошло не так',
            desc='Кажется, сегодня твоего сообщения никто не увидит)))'
        ).build_text())
        return await show_support_page(message)

    await state.update_data({'mail': mail})
    await message.answer(
        BasePage(
            title='Это все?',
            content='"{}"'.format(mail.text),
            desc='Если это окончательный вариант обращения, жми отправить'
        ).build_text(),
        reply_markup=build_user_send_message_kb()
    )


@router.callback_query(SupportMessageCallback.filter(F.action == SupportMessageAction.SEND_MESSAGE))
async def process_support_send_message(callback: types.CallbackQuery, state: FSMContext):
    userdata = await state.get_data()
    await state.clear()

    mail = userdata.get('mail')
    if mail is None:
        await callback.answer('хм...')
        return await callback.message.edit_text(
            ErrorPage(
                icon=icons.nerd_face,
                title='Прости, я потерял твое сообщение',
                content='Можешь написать его заново?'
            ).build_text()
        )

    if await support_service.create_mail(mail):
        await callback.answer('Готово')
        await callback.message.edit_text(
            BasePage(
                title='Сообщение отправлено',
                content='Ответ отправим через бота, а если забудем - сможешь получить его на странице /support'
            ).build_text()
        )
    else:
        await callback.answer('Не получилось')
        await callback.message.answer(ErrorPage(
            title='Что-то пошло не так',
            desc='Кажется, сегодня твоего сообщения никто не увидит)))'
        ).build_text())


@router.callback_query(SupportCallback.filter(F.action == SupportAction.BACK))
async def process_support_cancel_typing(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await show_support_page(callback.message, edit=True)


@router.callback_query(SupportCallback.filter(F.action == SupportAction.ALL_MESSAGES))
async def process_support_all_messages(callback: types.CallbackQuery, profile: Profile):
    await callback.answer()
    support_page = await SupportMailPage.create(profile)
    mails = await profile_service.get_mails(profile, offset=0, limit=10)
    await callback.message.edit_text(
        support_page.build_text(),
        reply_markup=build_user_support_messages_kb(mails)
    )


@router.callback_query(SupportMessageCallback.filter(F.action == SupportMessageAction.MESSAGE_DETAIL))
async def process_support_message_detail(
        callback: types.CallbackQuery,
        callback_data: SupportMessageCallback,
        profile: Profile
):
    mail = await support_service.get_or_none_by_id(callback_data.payload)
    if mail is None:
        await callback.answer('Ошибка')
        return await callback.message.edit_text(
            ErrorPage(
                title='Упс..',
                content='Такого сообщения больше нет',
            ).build_text(),
        )

    await callback.answer()
    mail_page = await SupportMailDetailPage.create(mail)
    await callback.message.edit_text(
        mail_page.build_text(),
        reply_markup=build_message_detail_kb()
    )


@router.callback_query(SupportAdminCallback.filter(F.action == SupportAdminAction.TYPE_ANSWER))
async def process_admin_type_answer_cb(
        callback: types.CallbackQuery,
        callback_data: SupportAdminCallback,
        state: FSMContext,
):
    await callback.answer()
    await state.set_state(SupportAdminState.answer_typing)
    await state.update_data({'mail_id': callback_data.payload})
    await callback.message.answer(
        BasePage(
            title='Ответить на сообщение',
            content='Напиши ответ пользователю, он получит уведомление сразу после отправки'
        ).build_text(),
        reply_markup=build_admin_support_type_answer_kb()
    )


@router.message(StateFilter(SupportAdminState.answer_typing))
async def process_admin_support_answer_type(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({'mail_answer': answer})
    await message.answer(BasePage(
        title='Отправить?',
        content='"{}"'.format(answer),
    ).build_text(), reply_markup=build_admin_support_type_answer_kb(include_send_answer=True))


@router.callback_query(SupportAdminCallback.filter(F.action == SupportAdminAction.SEND_ANSWER))
async def process_support_admin_send_answer(callback: types.CallbackQuery, state: FSMContext):
    userdata = await state.get_data()
    mail_answer, mail_id = userdata.get('mail_answer'), userdata.get('mail_id')

    await state.clear()
    await callback.answer()
    if not any([mail_answer, mail_id]):
        return await callback.message.answer(
            ErrorPage(title='error', content='not enough state data').build_text()
        )

    mail = await support_service.get_or_none_by_id(mail_id)
    if not mail:
        return await callback.message.answer(ErrorPage(
            title='Ошибка', content='Сообщения больше не существует'
        ).build_text())
    #
    # try:
    mail_instance = await support_service.create_answer_to_mail(mail, mail_answer)
    await callback.message.answer(BasePage(
        icon=icons.message_out,
        title='Ответ отправлен',
        content=mail_instance.text_short,
        desc=mail_instance.answer_short,
    ).build_text())
    # except Exception as e:
    #     await callback.message.answer(ErrorPage(
    #         title='Не отправлено',
    #         content=html_decoration.pre(str(e)),
    #     ).build_text())