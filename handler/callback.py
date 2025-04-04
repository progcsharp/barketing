import hashlib
import time

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from State.form import EditText, RefLinkStates
from config import ROBOKASSA_LOGIN, ROBOKASSA_PASS1
from db.handler.delete import delete_link
from db.handler.get import get_message, get_messages, get_links, get_link, check_pay_course
from db.handler.update import update_user
from handler.commands import admin_cmd
from payment.pay import process_payment, verify_robokassa_payment


async def call_step1(call: types.CallbackQuery):
    # await call.message.delete()

    builder = InlineKeyboardBuilder()

    # Основная кнопка
    builder.add(types.InlineKeyboardButton(
        text="Получить материалы",
        callback_data="step2")
    )

    # Настраиваем расположение кнопок (1 в ряд - вертикально)
    builder.adjust(1)

    # message_text = (
    #     "🎯 <b>Твои скрипты ЗДЕСЬ! Скачивай бесплатно!</b>\n"
    #     "(Доступ по ссылке ниже)\n\n"
    #     "━━━━━━━━━━━━━━━━━━━━━━━\n"
    #     "🌟 <b>Чем этот курс уникален?</b>\n\n"
    #     "▫️ <b>Создан продажником и маркетологом</b> в одном лице\n"
    #     "▫️ <b>Подходит как новичкам, так и профессионалам</b> - каждый найдет ценное\n"
    #     "▫️ <b>Пошаговая система</b> - весь материал от А до Я\n"
    #     "▫️ <b>Реальные кейсы</b> с живыми диалогами и аудио примерами\n"
    #     "▫️ <b>Пожизненный доступ</b> - учись в удобном темпе\n"
    #     "▫️ <b>Профессиональный видеоряд</b> - приятно смотреть и учиться\n\n"
    #     "━━━━━━━━━━━━━━━━━━━━━━━\n"
    #     "💡 Нажми 'Получить материалы' или посмотри трейлер курса!"
    # )
    message_text = await get_message("step2_text")
    link_video = await get_message("link_video")
    print(link_video)

    # Сначала отправляем видео
    await call.message.answer_video(
        video=link_video,
        caption=await get_message("text_video"),
        parse_mode="HTML"
    )

    # Затем отправляем текстовое сообщение с кнопками
    await call.message.answer(
        text=message_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


async def call_step2(call: types.CallbackQuery):
    # await call.message.delete()

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Стоимость курса",
        callback_data="step3")
    )

    # Единое красиво оформленное сообщение
    # message_text = (
    #     "🔮 <b>Доступ к курсу останется у тебя НАВСЕГДА!</b>\n\n"
    #     "Но уже через <b>3 ДНЯ</b> обучения (как и 95% моих учеников) ты:\n\n"
    #     "1️⃣ Научишься управлять голосом и интонацией, продавать эмоциями\n"
    #     "2️⃣ Перестанешь заканчивать разговор после «Я подумаю» от клиента\n"
    #     "3️⃣ Научишься «вести клиента за руку» и быть альфой в диалоге\n"
    #     "4️⃣ Поймешь важность использования скриптов в продажах\n"
    #     "5️⃣ Узнаешь как превратить клочок бумаги перед собой в живые деньги\n"
    #     "6️⃣ <b>НАЧНЕШЬ ЗАРАБАТЫВАТЬ ЗНАЧИТЕЛЬНО БОЛЬШЕ</b>, чем сейчас\n\n"
    #     "━━━━━━━━━━━━━━━━━━━━━━━\n"
    #     "💎 <i>Заманчивая перспектива?</i>\n"
    #     "Жми на кнопку ниже, чтобы увидеть программу и <b>СТОИМОСТЬ КУРСА</b>!"
    # )
    message_text = await get_message("step3_text")

    await call.message.answer(
        text=message_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


async def call_step3(call: types.CallbackQuery):
    # await call.message.delete()

    # Создаем клавиатуру с кнопками (вертикальное расположение)
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Тариф полный - 13 100 руб.",
            callback_data="fullprice"
        ),
        types.InlineKeyboardButton(
            text="Продажи от 0 до PRO - 9 450 руб.",
            callback_data="price2"
        ),
        types.InlineKeyboardButton(
            text="Спецкурс - 6 400 руб.",
            callback_data="Special course"
        )
    )

    builder.adjust(1)  # 1 кнопка в ряд → вертикально

    # Текст сообщения с HTML-разметкой
    # message_text = (
    #     "<b>Курс состоит из 11 профессионально отснятых видео-уроков</b> 🎥\n\n"
    #     "Что невероятно полезно (и отличает курс от других) — "
    #     "<b>доп. материалы с РЕАЛЬНЫМИ ПРИМЕРАМИ ДИАЛОГОВ</b> "
    #     "(аудио + переписки).\n\n"
    #     "----------------------------------\n"
    #     "<b>Почему это важно?</b>\n"
    #     "1. Приветствие и страх первого звонка / встречи\n"
    #     "2. Улыбка – твой бесплатный бустер\n"
    #     "3. Магия имени\n"
    #     "4. Записки сумасшедшего\n"
    #     "5. Ты профессионал? Стань им!\n"
    #     "6. Выявление истинной потребности клиента\n"
    #     "7. УТП и КП – что это и почему это важно?\n"
    #     "8. Работа с возражениями\n"
    #     "9. Фиксация сделки\n"
    #     "10. Завершение сделки\n\n"
    #     "----------------------------------\n"
    #     "💡 Уже через 3 дня ты сможешь закрывать сделки быстрее и увереннее!\n"
    #     "Всё, что нужно — нажать кнопку <b>«Оплатить»</b> ниже ⤵️"
    # )
    message_text = await get_message("step4_text")

    # Отправляем сообщение с фото и клавиатурой
    await call.message.answer(
        text=message_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


async def process_fullprice(callback: types.CallbackQuery):
    # await callback.message.delete()
    await process_payment(callback.message, 13100, "Полный тариф", "full")


async def process_price2(callback: types.CallbackQuery):
    # await callback.message.delete()
    await process_payment(callback.message, 9450, "Продажи от 0 до PRO", "pro")


async def process_special(callback: types.CallbackQuery):

    if check_pay_course(callback.from_user.id):
        await callback.message.answer("Данный курс доступен тольке после покупки тарифа 'Продажи от 0 до PRO'")
    else:
        await callback.message.delete()
        await process_payment(callback.message, 6400, "Спецкурс", "special")


# async def process_payment(message: types.Message, amount: int, product_name: str):
#
#
#     # Генерируем ссылку для оплаты через Robokassa
#     payment_url = generate_robokassa_link(
#         amount=amount,
#         description=product_name,
#         order_id=f"{message.from_user.id}_{int(time.time())}"
#     )
#
#     builder = InlineKeyboardBuilder()
#     builder.add(
#         types.InlineKeyboardButton(
#             text="💳 Оплатить",
#             url=payment_url
#         ),
#         types.InlineKeyboardButton(
#             text="✅ Я оплатил",
#             callback_data="check_payment"
#         )
#     )
#     builder.adjust(1)
#
#     message_text = await get_message("pay")
#     message_text = message_text.replace("?tariff_name", product_name)
#     message_text = message_text.replace("?price", amount)
#
#     await message.answer(
#         text=message_text,
#         reply_markup=builder.as_markup(),
#         parse_mode="HTML"
#     )
#
#
# def generate_robokassa_link(amount: int, description: str, order_id: str) -> str:
#     """Генерирует ссылку для оплаты через Robokassa"""
#     # Данные вашего магазина в Robokassa
#     merchant_login = ROBOKASSA_LOGIN
#     password1 = ROBOKASSA_PASS1  # Пароль 1 для тестовой среды
#
#     # Формируем подпись
#     signature = hashlib.md5(
#         f"{merchant_login}:{amount}:{order_id}:{password1}".encode()
#     ).hexdigest()
#
#     return (
#         f"https://auth.robokassa.ru/Merchant/Index.aspx?"
#         f"MerchantLogin={merchant_login}&"
#         f"OutSum={amount}&"
#         f"InvId={order_id}&"
#         f"Description={description}&"
#         f"SignatureValue={signature}&"
#         f"IsTest=1"  # 1 - для тестовой среды, 0 - для боевой
#     )


async def check_payment(callback: types.CallbackQuery):
    # Разбиваем callback_data на части
    _, order_id, tariff_name = callback.data.split(":")  # Получаем "check_payment:12345" → ["check_payment", "12345"]

    try:
        order_id = int(order_id)
        is_paid = True#await verify_robokassa_payment(order_id)
        if tariff_name in ["full", "pro"]:
            update_user(callback.from_user.id)

        if is_paid:
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(
                text="📥 Получить материалы",
                callback_data=f"get_materials:{tariff_name}"
            ))
            await callback.message.edit_text(
                text="✅ Платеж подтвержден!",
                reply_markup=builder.as_markup()
            )
        else:
            await callback.answer("Платеж еще не обработан. Попробуйте через минуту.", show_alert=True)

    except (ValueError, IndexError):
        await callback.answer("Ошибка проверки платежа", show_alert=True)


async def send_materials(callback: types.CallbackQuery):
    # await callback.message.delete()
    _, tariff_name = callback.data.split(":")

    # Здесь должна быть логика отправки материалов
    if tariff_name == "full":
        await callback.message.answer(
            text="<b>🎉 Ваши материалы готовы tariff_name = full!</b>\n\n"
                 "1. <a href='https://example.com/course.pdf'>Основной курс (PDF)</a>\n"
                 "2. <a href='https://example.com/bonus.zip'>Бонусные материалы</a>\n\n"
                 "Если возникли проблемы с доступом, напишите в поддержку.",
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    if tariff_name == "pro":
        await callback.message.answer(
            text="<b>🎉 Ваши материалы готовы tariff_name = pro!</b>\n\n"
                 "1. <a href='https://example.com/course.pdf'>Основной курс (PDF)</a>\n"
                 "2. <a href='https://example.com/bonus.zip'>Бонусные материалы</a>\n\n"
                 "Если возникли проблемы с доступом, напишите в поддержку.",
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    if tariff_name == "special":
        await callback.message.answer(
            text="<b>🎉 Ваши материалы готовы tariff_name = special!</b>\n\n"
                 "1. <a href='https://example.com/course.pdf'>Основной курс (PDF)</a>\n"
                 "2. <a href='https://example.com/bonus.zip'>Бонусные материалы</a>\n\n"
                 "Если возникли проблемы с доступом, напишите в поддержку.",
            parse_mode="HTML",
            disable_web_page_preview=True
        )


##admin

async def edit_texts_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки для каждого текстового блока
    for message in await get_messages():

        builder.add(
            types.InlineKeyboardButton(
                text=message.title,
                callback_data=f"edit_text_{message.slug}"
            )
        )

    # Кнопка возврата
    builder.add(
        types.InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="admin_back"
        )
    )

    builder.adjust(1)  # По одной кнопке в ряд

    await callback.message.edit_text(
        "📝 <b>Редактирование текстов</b>\n\n"
        "Выберите текст для изменения:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


async def show_text_to_edit(callback: types.CallbackQuery):
    text_slug = callback.data.split("_", 2)[-1]

    # Получаем текущий текст из БД (замените на ваш запрос)
    current_text = await get_message(text_slug)

    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="✏️ Изменить текст",
            callback_data=f"change_text_{text_slug}"
        ),
        types.InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="admin_edit_texts"
        )
    )

    await callback.message.edit_text(
        f"Текущее содержание:\n"
        f"------------------\n"
        f"{current_text}\n"
        f"------------------",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


async def request_new_text(callback: types.CallbackQuery, state: FSMContext):
    text_slug = callback.data.split("_", 2)[-1]
    await state.update_data({"slug": text_slug})
    await state.set_state(EditText.message)
    # Сохраняем slug текста в состоянии (можно использовать FSM)
    await callback.message.answer(
        f"Введите новый текст :\n"
        f"Можно использовать HTML-разметку",
        parse_mode="HTML"
    )


async def admin_back(callback: types.CallbackQuery):
    await callback.message.delete()
    await admin_cmd(callback.message)


async def ref_links_menu(callback: types.CallbackQuery):
    """Меню управления реферальными ссылками"""
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="📊 Посмотреть все ссылки",
            callback_data="view_ref_links"
        )
    )

    builder.row(
        types.InlineKeyboardButton(
            text="➕ Добавить ссылку",
            callback_data="add_ref_link"
        )
    )

    builder.row(
        types.InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="admin_back"
        )
    )

    await callback.message.edit_text(
        "🔗 <b>Управление реферальными ссылками</b>\n\n"
        "Выберите действие:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


async def view_ref_links(callback: types.CallbackQuery):
    """Просмотр всех реферальных ссылок"""

    links = await get_links()

    builder = InlineKeyboardBuilder()

    # Добавляем кнопки для каждой ссылки
    for link in links:
        builder.row(
            types.InlineKeyboardButton(
                text=f"{link.name} (использований: {link.count})",
                callback_data=f"ref_link_detail_{link.id}"
            )
        )

    builder.row(
        types.InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="admin_ref_links"
        )
    )

    await callback.message.edit_text(
        "📋 <b>Список реферальных ссылок</b>\n\n"
        "Выберите ссылку для детальной информации:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


async def ref_link_detail(callback: types.CallbackQuery):
    """Детальная информация о реферальной ссылке"""
    link_id = int(callback.data.split("_")[-1])
    link = await get_link(link_id)
    # Создаем клавиатуру
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="❌ Удалить ссылку",
            callback_data=f"delete_ref_link_{link.id}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="◀️ Назад к списку",
            callback_data="view_ref_links"
        )
    )

    # Формируем сообщение с информацией
    message_text = (
        "🔍 <b>Детальная информация о ссылке</b>\n\n"
        f"<b>Название:</b> {link.name}\n"
        f"<b>Использований:</b> {link.count}\n"
        f"<b>Полная ссылка:</b>\n"
        f"<code>https://t.me/Test_12_12_12345_bot?start={link.url}</code>"
    )

    await callback.message.edit_text(
        text=message_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


async def confirm_delete(callback: types.CallbackQuery):
    """Подтверждение удаления ссылки"""
    link_id = int(callback.data.split("_")[-1])
    link = await delete_link(link_id)

    if link:
        await callback.message.edit_text(
            text=f"✅ Ссылка <b>{link.name}</b> успешно удалена!",
            parse_mode="HTML"
        )

        # Возвращаемся к списку ссылок
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(
                text="◀️ Назад к списку",
                callback_data="view_ref_links"
            )
        )
        await callback.message.edit_reply_markup(
            reply_markup=builder.as_markup()
        )
    else:
        await callback.answer("Ссылка уже удалена", show_alert=True)


async def add_ref_link_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RefLinkStates.waiting_for_name)
    await callback.message.edit_text(
        "✏️ Введите название для новой реферальной ссылки:",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[
                types.InlineKeyboardButton(
                    text="◀️ Отмена",
                    callback_data="cancel_ref_creation"
                )
            ]]
        )
    )


async def cancel_ref_creation(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await ref_links_menu(callback)
