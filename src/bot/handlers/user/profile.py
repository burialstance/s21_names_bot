from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration

from src.bot.middlewares.profile import ProfileMiddleware
from src.bot.states.profile import ProfileState
from src.models.profile import Profile
from src.services import profile as profile_service
from src.bot.pages.profile import ProfilePage
from src.bot.keyboards.inline.profile import (
    build_profile_private_kb,
    build_delete_profile_kb,
    ProfileAction,
    ProfileCallback,
)

router = Router()
router.message.outer_middleware.register(ProfileMiddleware(required=True))
router.callback_query.outer_middleware.register(ProfileMiddleware(required=True))


@router.message(Command(commands=['profile']))
async def on_profile(message: types.Message, profile: Profile):
    profile_page = await ProfilePage.create(profile=profile)

    await message.answer(
        text=profile_page.build_text(),
        reply_markup=build_profile_private_kb()
    )


@router.message(Command(commands=['delete']))
async def on_delete(message: types.Message):
    await message.answer(
        text='\n'.join([
            'Ты уверен, что собираешься удалить свой профиль?',
            html_decoration.bold('Это действие необратимо.')
        ]),
        reply_markup=build_delete_profile_kb()
    )


@router.callback_query(ProfileCallback.filter(F.action == ProfileAction.DELETE))
async def process_delete_profile_cb(callback: types.CallbackQuery, profile: Profile):
    await callback.answer()
    if await profile_service.delete_cascade(profile):
        await callback.message.answer('У тебя получилось, профиль удален')
    else:
        await callback.message.answer('Что-то пошло не так. профиль не удален')


@router.callback_query(ProfileCallback.filter(F.action == ProfileAction.SCHOOL_USERNAME_CHANGE))
async def process_telegram_username_change_cb(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ProfileState.set_s21_login)
    await callback.message.answer('Ок. Давай сменим твой школьный логин. отправь в следующем сообщении новый логин')


@router.message(StateFilter(ProfileState.set_s21_login))
async def process_update_profile_school_username(message: types.Message, state: FSMContext):
    await message.answer(
        f'изменение логинов еще не привезли, зато ты можешь удалить свой профиль)) {message.text}',
        reply_markup=build_delete_profile_kb()
    )


@router.callback_query(ProfileCallback.filter(F.action == ProfileAction.TELEGRAM_USERNAME_CHANGE))
async def process_telegram_username_change_cb(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ProfileState.set_telegram_login)
    await callback.message.answer('Ок. Давай сменим твой телеграм логин. отправь в следующем сообщении новый логин')


@router.message(StateFilter(ProfileState.set_telegram_login))
async def process_update_profile_telegram_username(message: types.Message, state: FSMContext):
    await message.answer(
        f'изменение логинов еще не привезли, зато ты можешь удалить свой профиль)) {message.text}',
        reply_markup=build_delete_profile_kb()
    )
