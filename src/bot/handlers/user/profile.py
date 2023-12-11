import textwrap

from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration

from src.bot.middlewares.profile import ProfileMiddleware
from src.bot.pages.base import BasePage
from src.bot.pages.error import ErrorPage
from src.bot.states.profile import ProfileState
from src.models.profile import Profile
from src.models.school import SchoolUserCreate
from src.models.telegram import TelegramUserCreate
from src.services import profile as profile_service
from src.services.school import user as school_user_service
from src.services.telegram import user as telegram_user_service
from src.bot.pages.profile import ProfilePage
from src.bot.misc import commands, icons
from src.bot.keyboards.inline.profile import (
    build_profile_private_kb,
    build_delete_profile_kb,
    build_approve_delete_profile_kb,
    build_setup_school_login_kb,
    build_setup_telegram_login_kb,
    ProfileAction,
    ProfileCallback,
)

router = Router()
router.message.outer_middleware.register(ProfileMiddleware(required=True))
router.callback_query.outer_middleware.register(ProfileMiddleware(required=True))


async def show_profile(message: types.Message, profile: Profile, edit: bool = False):
    profile_page = await ProfilePage.create(profile=profile)

    text = profile_page.build_text()
    reply_markup = build_profile_private_kb()

    if not edit:
        await message.answer(text, reply_markup=reply_markup)
    else:
        await message.edit_text(text, reply_markup=reply_markup)


@router.message(Command(commands=[commands.PROFILE_CMD]))
async def on_profile(message: types.Message, profile: Profile):
    await show_profile(message, profile)


@router.callback_query(ProfileCallback.filter(F.action == ProfileAction.BACK_TO_PROFILE))
async def process_back_to_profile(callback: types.CallbackQuery, state: FSMContext, profile: Profile):
    await callback.answer()
    await state.clear()
    await show_profile(callback.message, profile, edit=True)


@router.message(Command(commands=[commands.DELETE_CMD]))
async def on_delete(message: types.Message):
    await message.answer(
        ErrorPage(
            title='Ты уверен, что собираешься удалить свой профиль?',
            desc='Это действие необратимо',
        ).build_text(),
        reply_markup=build_delete_profile_kb()
    )


@router.callback_query(ProfileCallback.filter(F.action == ProfileAction.DELETE))
async def process_delete_profile_cb(callback: types.CallbackQuery):
    await callback.answer('Подтверди удаление (:')
    await callback.message.edit_reply_markup(reply_markup=build_approve_delete_profile_kb())


@router.callback_query(ProfileCallback.filter(F.action == ProfileAction.APPROVE_DELETE))
async def process_delete_profile_cb(callback: types.CallbackQuery, profile: Profile):
    await callback.answer()
    await callback.message.delete()
    if await profile_service.delete_cascade(profile):
        await callback.message.answer(BasePage(
            title='У тебя получилось, профиль удален',
            desc='Если захочешь вернуться, пиши /start и пройди регистрацию заново'
        ).build_text())
    else:
        await callback.message.answer(ErrorPage(title='Что-то пошло не так. профиль не удален').build_text())


@router.callback_query(ProfileCallback.filter(F.action == ProfileAction.SCHOOL_USERNAME_CHANGE))
async def process_telegram_username_change_cb(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ProfileState.set_s21_login)
    await callback.message.edit_text(BasePage(
        title='Изменение школьного логина',
        content='Отправь в следующем сообщении новый логин'
    ).build_text(), reply_markup=build_setup_school_login_kb())


@router.message(StateFilter(ProfileState.set_s21_login))
async def process_update_profile_school_username(message: types.Message, state: FSMContext, profile: Profile):
    try:
        school_user = SchoolUserCreate(username=message.text)
    except ValueError:
        return await message.answer(
            ErrorPage(
                title='Это не похоже на логин с платформы',
                content='"{}"'.format(textwrap.shorten(message.text, 32))
            ).build_text()
        )

    if profile_exist := await profile_service.get_or_none_by_school_username(school_user.username):
        if profile_exist != profile:
            await profile_exist.fetch_related('telegram_user')
            return await message.answer(ErrorPage(
                title='Этот логин уже использует другой пользователь',
                content=f'Свяжись с @{profile_exist.telegram_user.username}.'
            ).build_text())

    await state.clear()
    await profile.fetch_related('school_user')
    try:
        await school_user_service.set_username(profile.school_user, school_user.username)
        await show_profile(message, profile, edit=False)
    except Exception:
        await message.answer(ErrorPage(title='Не удалось изменить логин', desc='сори у меня лапки))').build_text())
        raise


@router.callback_query(ProfileCallback.filter(F.action == ProfileAction.TELEGRAM_USERNAME_CHANGE))
async def process_telegram_username_change_cb(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ProfileState.set_telegram_login)
    await callback.message.edit_text(
        BasePage(
            title='Изменение телеграм логина',
            content='Отправь в следующем сообщении новый логин'
        ).build_text(),
        reply_markup=build_setup_telegram_login_kb(default_username=callback.from_user.username)
    )


@router.callback_query(ProfileCallback.filter(F.action == ProfileAction.SET_TELEGRAM_USERNAME))
async def process_set_telegram_username_cb(callback: types.CallbackQuery, state: FSMContext, profile: Profile):
    username = callback.from_user.username

    if username is None:  # if user made profile private after getting the btn
        await callback.answer('Хммм...')
        return await callback.message.answer(ErrorPage(
            icon=icons.nerd_face,
            title='Твой логин в телеграме не доступен',
            content='Измени настройки приватности или отправь логин вручную'
        ).build_text())

    await state.clear()
    await profile.fetch_related('telegram_user')

    if profile.telegram_user.username != username:
        await telegram_user_service.set_username(profile.telegram_user, username)
        await callback.answer('Изменения применены')
    else:
        await callback.answer('Ничего не изменилось))')

    await show_profile(callback.message, profile, edit=True)


@router.message(StateFilter(ProfileState.set_telegram_login))
async def process_update_profile_telegram_username(message: types.Message, state: FSMContext, profile: Profile):
    try:
        telegram_user = TelegramUserCreate(id=message.from_user.id, username=message.text)
    except ValueError:
        return await message.answer(
            ErrorPage(
                title='Это не похоже на логин телеграма',
                content='"{}"'.format(textwrap.shorten(message.text, 32))
            ).build_text()
        )

    if profile_exist := await profile_service.get_or_none_by_school_username(telegram_user.username):
        if profile_exist != profile:
            return await message.answer(
                ErrorPage(
                    title='Этот логин уже использует другой пользователь',
                    content=f'Свяжись с @{profile_exist.telegram_user.username}.'
                ).build_text()
            )

    await state.clear()
    await profile.fetch_related('telegram_user')
    try:
        await telegram_user_service.set_username(profile.telegram_user, telegram_user.username)
        await show_profile(message, profile)

    except Exception as e:
        await message.answer(ErrorPage(
            title='Не удалось изменить логин',
            desc='сори у меня лапки))',
        ).build_text())
        raise
