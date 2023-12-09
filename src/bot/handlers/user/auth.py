import textwrap

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from aiogram.utils.text_decorations import html_decoration

from src.bot.pages.error import ErrorPage
from src.bot.pages.base import BasePage
from src.models.profile import ProfileCreate
from src.bot.misc import icons
from src.bot.states.auth import UserRegistration
from src.bot.keyboards.inline.auth import AuthAction, AuthCallback, build_finish_register_kb, build_register_kb
from src.models.telegram import TelegramUserCreate
from src.models.school import SchoolUserCreate
from src.services import profile as profile_service

router = Router()


@router.callback_query(AuthCallback.filter(F.action == AuthAction.REGISTER))
async def process_register_cb(callback: types.CallbackQuery, state: FSMContext):
    if await profile_service.get_or_none_by_telegram_user_id(callback.from_user.id) is not None:
        await callback.message.delete()
        return await callback.answer(
            ErrorPage(title='Регистрация уже завершена').build_text(disable_decoration=True),
            show_alert=True
        )

    await callback.answer()

    if callback.from_user.username is None:
        await state.set_state(UserRegistration.set_telegram_login)
        return await callback.message.answer(
            ErrorPage(
                title='Кажется, в телеграме у тебя скрыт username',
                content='Отправь мне его и сможем двигаться дальше (:'
            ).build_text()
        )

    await state.update_data({
        'telegram_user': TelegramUserCreate.model_validate(callback.from_user, from_attributes=True)
    })
    await state.set_state(UserRegistration.set_s21_login)
    await callback.message.answer(
        BasePage(
            title='Введи свой школьный ник с платформы',
            content='например tyberora или tyberora@student.21-school.ru'
        ).build_text(),
        disable_web_page_preview=True,
    )


@router.message(StateFilter(UserRegistration.set_telegram_login))
async def process_telegram_login_setup(message: types.Message, state: FSMContext):
    try:
        telegram_user = TelegramUserCreate(id=message.from_user.id, username=message.text)
    except ValueError:
        await message.answer(ErrorPage(icon=icons.dont_know, title='Это не похоже на логин телеграмма').build_text())
        raise

    await state.update_data({'telegram_user': telegram_user})

    await state.set_state(UserRegistration.set_s21_login)
    await message.answer(BasePage(title='А теперь отправь свой школьный ник с платформы').build_text())


@router.message(StateFilter(UserRegistration.set_s21_login))
async def process_s21_login_setup(message: types.Message, state: FSMContext):
    try:
        school_user = SchoolUserCreate(username=message.text)
    except ValueError:
        return await message.answer(
            ErrorPage(
                title='Это не похоже на логин с платформы',
                content='"{}"'.format(textwrap.shorten(message.text, 32))
            ).build_text()
        )

    if profile := await profile_service.get_or_none_by_school_username(school_user.username):
        await profile.fetch_related('telegram_user')
        return await message.answer(
            ErrorPage(
                title='Этот логин уже использует другой пользователь',
                content=f'Свяжись с @{profile.telegram_user.username}.'
            ).build_text()
        )

    await state.update_data({'school_user': school_user})
    userdata = await state.get_data()
    await message.answer(
        BasePage(
            title='Почти готово но небольшой ахтунг',
            content=html_decoration.pre('\n'.join([
                f'school username: {userdata.get("school_user").username}',
                f'telegram username: {userdata.get("telegram_user").username}'
            ])),
            desc='Если {} открывается не твой профиль, отправь исправленный логин в следующем сообщении'.format(
                html_decoration.link('по этой ссылке', school_user.profile_url)
            )
        ).build_text(),
        reply_markup=build_finish_register_kb()
    )


@router.callback_query(AuthCallback.filter(F.action == AuthAction.REGISTER_FINISH))
async def process_finish_registration(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    user_data: dict = await state.get_data()
    await state.clear()

    if not user_data:
        return await callback.message.answer(
            ErrorPage(
                icons=icons.dont_know,
                title='Уппс..',
                content='Я случайно потерял твои регистрационные данные, отправь их заново (:'
            ).build_text(),
            reply_markup=build_register_kb()
        )
    else:
        await profile_service.create(ProfileCreate(**user_data))
        await callback.message.answer(
            BasePage(
                title='Регистрация завершена.',
                content='Твой профиль доступен тут /profile',
                desc=' '.join([
                    'Теперь отправь мне логин с одной из платформ, а я попробую что-нибудь найти', icons.nerd_face
                ])
            ).build_text()
        )
