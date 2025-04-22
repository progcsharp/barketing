from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from State.form import RefLinkStates
from config import bot, ADMIN_ID
from db.handler.create import create_link
from db.handler.update import update_message, update_tariff_price


async def message_edit_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    slug = data["slug"]
    media_slugs = ["link_photo", "link_video"]  # Слаги, которые ожидают медиа

    try:
        if slug in media_slugs:
            # Обработка медиа
            if message.photo:
                # Если прислали фото - берем последнее (самое высокое качество)
                file_id = message.photo[-1].file_id
            elif message.video:
                # Если прислали видео
                file_id = message.video.file_id
            else:
                # Если прислали что-то другое, когда ожидали медиа
                update_message(slug, message.text)
                await message.answer("Текст успешно изменен")
                await state.clear()
                return

            # Обновляем в базе file_id
            update_message(slug, file_id)
            await message.answer(f"Медиа для {slug} успешно обновлено!")

        else:
            # Обработка обычного текста
            if not message.text:
                await message.answer("Пожалуйста, отправьте текстовое сообщение")
                return

            update_message(slug, message.text)
            await message.answer("Текст успешно изменен")

        await state.clear()

    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
        await state.clear()


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
    await state.clear()
    await message.answer(
        f"Реферальная ссылка успешно создана",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


async def handle_new_price(message: types.Message, state: FSMContext):
    try:
        new_price = float(message.text)
        if new_price <= 0:
            raise ValueError("Цена должна быть больше 0")
    except ValueError:
        await message.answer("Пожалуйста, введите корректную цену (число больше 0):")
        return

    data = await state.get_data()
    tariff_name = data.get('tariff_name')

    # Здесь должна быть логика обновления цены в базе данных
    # Например:
    await update_tariff_price(tariff_name, new_price)

    await message.answer(f"✅ Цена для тарифа {tariff_name.capitalize()} успешно изменена на {new_price}")
    await state.clear()
