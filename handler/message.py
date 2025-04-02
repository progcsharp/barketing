from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from State.form import RefLinkStates
from config import bot, ADMIN_ID
from db.handler.create import create_link
from db.handler.update import update_message


async def message_edit_text(message: types.Message, state: FSMContext):
    slug = dict(await state.get_data())["slug"]
    update_message(slug, message.text)
    await message.answer(f"Текст успещшно изменен")


async def process_ref_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RefLinkStates.waiting_for_token)

    await message.answer(
        f"Введите реферальный код",
        parse_mode="HTML"
    )


async def process_ref_token(message: types.Message, state: FSMContext):
    await state.update_data(token=message.text)
    await state.set_state(RefLinkStates.waiting_for_token)

    data = await state.get_data()
    await create_link(url=data['token'], name=data['name'])
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="admin_back"
        )
    )

    await message.answer(
        f"Реферальная ссылка успешно создана",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
