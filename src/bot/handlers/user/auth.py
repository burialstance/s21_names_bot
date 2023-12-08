import textwrap

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from aiogram.utils.text_decorations import html_decoration

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
        return await callback.answer(' '.join([icons.warning, 'Регистрация уже завершена.']), show_alert=True)

    await callback.answer()

    if callback.from_user.username is None:
        await state.set_state(UserRegistration.set_telegram_login)
        return await callback.message.answer(' '.join([
            'Кажется, в телеграме у тебя скрыт username.',
            'Отправь мне его и сможем двигаться дальше (:'
        ]))

    await state.update_data({
        'telegram_user': TelegramUserCreate.model_validate(callback.from_user, from_attributes=True)
    })
    await state.set_state(UserRegistration.set_s21_login)
    await callback.message.answer('Введи свой школьный ник с платформы')


@router.message(StateFilter(UserRegistration.set_telegram_login))
async def process_telegram_login_setup(message: types.Message, state: FSMContext):
    try:
        telegram_user = TelegramUserCreate(id=message.from_user.id, username=message.text)
    except Exception as e:
        await message.answer(str(e))
        raise

    await state.update_data({'telegram_user': telegram_user})

    await state.set_state(UserRegistration.set_s21_login)
    await message.answer('А теперь отправь свой школьный ник с платформы')


@router.message(StateFilter(UserRegistration.set_s21_login))
async def process_s21_login_setup(message: types.Message, state: FSMContext):
    try:
        school_user = SchoolUserCreate(username=message.text)
    except ValueError:
        return await message.answer('\n'.join([
            ' '.join([icons.warning, html_decoration.bold('Это не похоже на логин с платформы')]),
            '',
            f'"{textwrap.shorten(html_decoration.italic(message.text), 32)}"',
        ]))

    if profile := await profile_service.get_or_none_by_school_username(school_user.username):
        await profile.fetch_related('telegram_user')
        return await message.answer('\n'.join([
            ' '.join([icons.warning, html_decoration.bold('Этот логин уже использует другой пользователь')]),
            '',
            f'Свяжись с @{profile.telegram_user.username}.'
        ]))

    await state.update_data({'school_user': school_user})
    await message.answer('\n'.join([
        html_decoration.pre(school_user.username),
        'Все оки-доки?',
        html_decoration.italic(
            'Если {} открывается не твой профиль, отправь исправленный логин в следующем сообщении'.format(
                html_decoration.link('по этой ссылке', school_user.profile_url)
            )
        )
    ]), reply_markup=build_finish_register_kb())


@router.callback_query(AuthCallback.filter(F.action == AuthAction.REGISTER_FINISH))
async def process_finish_registration(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    user_data: dict = await state.get_data()
    await state.clear()

    print(user_data)
    if not user_data:
        return await callback.message.answer(
            'Я случайно потерял твои регистрационные данные, отправь их заново (:',
            reply_markup=build_register_kb()
        )
    else:
        await profile_service.create(ProfileCreate(**user_data))
        await callback.message.answer('\n'.join([
            html_decoration.bold('Регистрация завершена.'),
            'Теперь отправь мне логин с одной из платформ, а я попробую что-нибудь найти'
            # *[f'{html_decoration.bold(key)}: {value}' for key, value in user_data.items()]
        ]))
