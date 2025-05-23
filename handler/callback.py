import hashlib
import time

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatInviteLink
from aiogram.utils.keyboard import InlineKeyboardBuilder

from State.form import EditText, RefLinkStates, ChangePriceState
from config import ROBOKASSA_LOGIN, ROBOKASSA_PASS1, bot, CHANNEL_ID1, CHANNEL_ID2, ADMIN_ID
from db.handler.delete import delete_link
from db.handler.get import get_message, get_messages, get_links, get_link, check_pay_course, get_tariff
from db.handler.update import update_user, update_link_pay_count
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
    full = await get_tariff("full")
    pro = await get_tariff("pro")
    special = await get_tariff("special")
    # Создаем клавиатуру с кнопками (вертикальное расположение)
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text=f"Тариф полный - {full.price} руб.",
            callback_data="fullprice"
        ),
        types.InlineKeyboardButton(
            text=f"Продажи от 0 до PRO - {pro.price} руб.",
            callback_data="price2"
        ),
        types.InlineKeyboardButton(
            text=f"Спецкурс - {special.price} руб.",
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
    tariff = await get_tariff("full")
    await process_payment(callback.message, tariff.price, "Полный тариф", tariff.tariff_name)


async def process_price2(callback: types.CallbackQuery):
    # await callback.message.delete()
    tariff = await get_tariff("pro")
    await process_payment(callback.message, tariff.price, "Продажи от 0 до PRO", tariff.tariff_name)


async def process_special(callback: types.CallbackQuery):

    if check_pay_course(callback.from_user.id):
        await callback.message.answer("Данный курс доступен тольке после покупки тарифа 'Продажи от 0 до PRO'")
    else:
        tariff = await get_tariff("special")
        await process_payment(callback.message, tariff.price, "Спецкурс", tariff.tariff_name)


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
            update_link_pay_count(callback.from_user.id, tariff_name)
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(
                text="📥 Получить материалы",
                callback_data=f"get_materials:{tariff_name}"
            ))
            await callback.message.edit_text(
                text="✅ Платеж подтвержден!",
                reply_markup=builder.as_markup()
            )
            for admin_id in ADMIN_ID:
                await bot.send_message(admin_id, f"Пользователь {callback.from_user.username} оплатил тарифф {tariff_name}")
        else:
            await callback.answer("Платеж еще не обработан. Попробуйте через минуту.", show_alert=True)

    except (ValueError, IndexError):
        await callback.answer("Ошибка проверки платежа", show_alert=True)


async def send_materials(callback: types.CallbackQuery):
    await callback.message.delete()
    _, tariff_name = callback.data.split(":")

    # Создаем одноразовую ссылку в канал
    invite_link_1channel: ChatInviteLink = await bot.create_chat_invite_link(
        chat_id=CHANNEL_ID1,
        name=f"Доступ для {callback.from_user.full_name} ({tariff_name})",
        member_limit=1,  # Ссылка работает только 1 раз
        creates_join_request=False,
    )
    invite_link_2channel: ChatInviteLink = await bot.create_chat_invite_link(
        chat_id=CHANNEL_ID2,
        name=f"Доступ для {callback.from_user.full_name} ({tariff_name})",
        member_limit=1,  # Ссылка работает только 1 раз
        creates_join_request=False,
    )

    # pay_full = await get_message("pay_full")
    # pay_full = pay_full.replace("?link_course",invite_link_1channel.invite_link)
    # pay_full = pay_full.replace("?link_special",invite_link_2channel.invite_link)

    # Отправляем материалы + ссылку
    if tariff_name == "full":
        pay_message = await get_message("pay_full")
        pay_message = pay_message.replace("?link_course", invite_link_1channel.invite_link)
        pay_message = pay_message.replace("?link_special", invite_link_2channel.invite_link)
        await callback.message.answer(
            text=pay_message,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    elif tariff_name == "pro":
        pay_message = await get_message("pay_pro")
        pay_message = pay_message.replace("?link_course", invite_link_1channel.invite_link)
        await callback.message.answer(
            text=pay_message,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    elif tariff_name == "special":
        pay_message = await get_message("pay_special")
        pay_message = pay_message.replace("?link_special", invite_link_2channel.invite_link)
        await callback.message.answer(
            text=pay_message,
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
        reply_markup=builder.as_markup()
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
    if not (callback.from_user.id in ADMIN_ID):
        # await callback.message.answer("⛔ У вас нет прав администратора")
        return

    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="✏️ Изменить текста",
            callback_data="admin_edit_texts"
        ),
        types.InlineKeyboardButton(
            text="🔗 Реферальные ссылки",
            callback_data="admin_ref_links"
        ),
        types.InlineKeyboardButton(
            text="Изменить цену",
            callback_data="admin_change_price"
        )
    )
    builder.adjust(1)  # По одной кнопке в ряд

    await callback.message.answer(
        "🛠️ <b>Административная панель</b>\n\n"
        "Выберите действие:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


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
                text=f"{link.name} (использований: {link.count}/{link.pay_count})",
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
        f"<code>https://t.me/barketing_bot?start={link.url}</code>"
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


async def handle_change_price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    # Добавляем кнопки с тарифами
    builder.add(
        types.InlineKeyboardButton(
            text="Тариф полный",
            callback_data="change_price_full"
        ),
        types.InlineKeyboardButton(
            text="Продажи от 0 до PRO",
            callback_data="change_price_pro"
        ),
        types.InlineKeyboardButton(
            text="Спецкурс",
            callback_data="change_price_special"
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="admin_back"
        )
    )
    builder.adjust(1)  # По одной кнопке в ряд

    await callback.message.answer(
        "Выберите тариф, для которого хотите изменить цену:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(ChangePriceState.waiting_for_tariff)
    await callback.answer()


async def handle_tariff_selection(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    tariff_map = {
        "change_price_full": "full",
        "change_price_pro": "pro",
        "change_price_special": "special"
    }

    tariff_key = callback.data
    tariff_name = tariff_map.get(tariff_key)

    if not tariff_name:
        await callback.answer("Неизвестный тариф")
        return

    await state.update_data(tariff_name=tariff_name)
    await callback.message.answer(f"Введите новую цену для тарифа {tariff_name.capitalize()}:")
    await state.set_state(ChangePriceState.waiting_for_new_price)
    await callback.answer()
