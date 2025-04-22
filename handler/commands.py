from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_ID
from db.handler.create import create_user
from db.handler.get import get_user_by_tg_id, get_message, get_tariff
# from handler.callback import process_payment
from db.handler.update import update_link
from payment.pay import process_payment


async def cmd_start(message: types.Message):
    print(message.from_user.id)
    # Проверка и создание пользователя
    if await get_user_by_tg_id(message.from_user.id):
        await create_user(tg_id=message.from_user.id, nickname=message.from_user.username)

    # print(message.text.split()[1])
    # await message.answer(message.text)
    command_args = message.text.split()
    # Создаем клавиатуру с кнопкой
    if len(command_args) > 1:
        # Обработка разных вариантов старта
        start_param = command_args[1]

        if await get_user_by_tg_id(message.from_user.id):
            update_link(message.from_user.id, start_param)

        if start_param == "full":
            tariff = await get_tariff("full")
            await process_payment(message, tariff.price, "Полный тариф", tariff.tariff_name)
        elif start_param == "pro":
            tariff = await get_tariff("pro")
            await process_payment(message, tariff.price, "Продажи от 0 до PRO", tariff.tariff_name)
        elif start_param == "special":
            tariff = await get_tariff("special")
            await process_payment(message, tariff.price, "Спецкурс", tariff.tariff_name)
        else:
            await normal_start(message)
    else:
        await normal_start(message)


async def normal_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Получить материалы",
        callback_data="step1")
    )

    # message_photo = (f"<b>Привет, {message.from_user.first_name}!</b>\n\n"
    #                  "Меня зовут Атем Бабкин, и я 12 лет в продажах! "
    #                  "Много о себе говорить не буду, лучше - о тебе. ")
    message_photo = await get_message("start_text_photo")
    message_photo = message_photo.replace("?name_user", message.from_user.first_name)
    # Формируем красивое сообщение с HTML-разметкой
    # welcome_text = (
    #     "Ведь ты здесь не случайно! Этот курс точно подойдет для тебя, если ты:\n\n"
    #
    #     "🔹 <b>В поисках себя</b>\n"
    #     "Ты твердо решил сменить сферу деятельности и уйти в продажи. "
    #     "Банально не знаешь с чего начать, чувствуешь себя не в своей тарелке "
    #     "и просто не решаешься начать продавать.\n\n"
    #
    #     "🔹 <b>Стеснительный молчун</b>\n"
    #     "Не решаешься совершить деловой звонок, а когда звонят тебе, "
    #     "то у тебя дрожит голос и трясутся руки. Понимаешь, что так ты далеко "
    #     "не уедешь и ищешь кто бы тебе помог.\n\n"
    #
    #     "🔹 <b>Скромный новичок</b>\n"
    #     "Ты совсем недавно работаешь в продажах и боишься делать первые шаги. "
    #     "Чувствуешь, что что-то делаешь не так, но не понимаешь над чем работать.\n\n"
    #
    #     "🔹 <b>Бывалый продажник</b>\n"
    #     "Ты давно продаешь товары и услуги, но уперся в «планку дохода». "
    #     "Не понимаешь как начать зарабатывать больше, как выйти на новый для себя уровень.\n\n"
    #
    #     "🔹 <b>Слабое звено</b>\n"
    #     "Ты ясно понимаешь, что в своем коллективе ты находишься в числе отстающих. "
    #     "Но это не в твоих правилах - проигрывать! Ты не опускаешь руки, "
    #     "а наоборот - хочешь стать лучше!\n\n"
    #
    #     "🔹 <b>Трудоголик в найме</b>\n"
    #     "Всегда берешь не качеством, а количеством. Устал бегать как белка в колесе "
    #     "и хочешь начать зарабатывать больше не «упахиваясь» как ты обычно делаешь.\n\n"
    #
    #     "🔹 <b>Владелец бизнеса</b>\n"
    #     "Ты хочешь улучшить эффективность работы своего штата продавцов-консультантов. "
    #     "Прекрасно понимаешь, что твоя прибыль увеличится только с ростом объема продаж.\n\n"
    #
    #     "<b>Узнал здесь себя?</b> Нажимай кнопку <b>'Получить материалы'</b> и забирай "
    #     "<b>БЕСПЛАТНО</b> скрипты для продаж, которые сможешь применять уже сегодня!"
    # )

    welcome_text = await get_message("start_text")
    link_photo = await get_message("link_photo")

    # Отправляем сообщение с фото и текстом
    await message.answer_photo(
        photo=link_photo,
        # Замените на реальный file_id или URL фото
        caption=message_photo,
        parse_mode="HTML"
    )

    await message.answer(
        text=welcome_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


async def admin_cmd(message: types.Message):
    print(message.from_user.id)
    if not(message.from_user.id in ADMIN_ID):
        # await message.answer("⛔ У вас нет прав администратора")
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

    await message.answer(
        "🛠️ <b>Административная панель</b>\n\n"
        "Выберите действие:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


async def cmd_about(message: types.Message):
    mess = await get_message("about")
    await message.answer(mess,
                         parse_mode="HTML"
                         )
