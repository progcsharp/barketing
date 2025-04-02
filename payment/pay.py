import hashlib
import time
import requests
from urllib.parse import quote

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ROBOKASSA_LOGIN, ROBOKASSA_PASS1, ROBOKASSA_PASS2
from db.handler.get import get_message


async def process_payment(message: types.Message, amount: int, product_name: str, tariff_name: str):
    """Генерация платежной ссылки Robokassa"""

    order_id = int(time.time())
    payment_url = generate_robokassa_link(
        amount=amount,
        description=product_name,
        order_id=order_id  # Только цифры!
    )

    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="💳 Оплатить",
            url=payment_url
        ),
        types.InlineKeyboardButton(
            text="✅ Я оплатил",
            callback_data=f"check_payment:{order_id}:{tariff_name}"
        )
    )
    builder.adjust(1)

    message_text = await get_message("pay")
    message_text = message_text.replace("?tariff_name", product_name)
    message_text = message_text.replace("?price", str(amount))

    await message.answer(
        text=message_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


def generate_robokassa_link(amount: int, description: str, order_id: int) -> str:
    """Генерирует ссылку для оплаты через Robokassa"""
    merchant_login = ROBOKASSA_LOGIN
    password1 = ROBOKASSA_PASS1

    # Формирование подписи (обязательно upper())
    signature = hashlib.md5(
        f"{merchant_login}:{amount}:{order_id}:{password1}".encode()
    ).hexdigest().upper()

    # URL-encode описание
    description_encoded = quote(description)

    return (
        f"https://auth.robokassa.ru/Merchant/Index.aspx?"
        f"MerchantLogin={merchant_login}&"
        f"OutSum={amount}&"
        f"InvId={order_id}&"
        f"Description={description_encoded}&"
        f"SignatureValue={signature}&"
        f"IncCurrLabel=RUB&"  # Валюта
        f"IsTest=1"  # 1 - тест, 0 - боевой режим
    )


async def verify_robokassa_payment(order_id: int) -> bool:
    """Проверяет статус платежа через API Robokassa"""
    try:
        # Параметры запроса
        params = {
            'MerchantLogin': ROBOKASSA_LOGIN,
            'InvoiceID': order_id,
            'Signature': generate_robokassa_signature(order_id)
        }

        # Отправляем запрос к API Robokassa
        response = requests.get(
            'https://auth.robokassa.ru/Merchant/WebService/Service.asmx/OpState',
            params=params
        )
        response.raise_for_status()

        # Парсим XML ответ (пример: <StateResponse><Code>0</Code></StateResponse>)
        if 'Code>0</Code' in response.text:
            return True
    except Exception as e:
        print(f"Error checking payment: {e}")
    return False


def generate_robokassa_signature(order_id: int) -> str:
    """Генерирует подпись для проверки платежа"""
    signature_str = f"{ROBOKASSA_LOGIN}:{order_id}:{ROBOKASSA_PASS2}"
    return hashlib.md5(signature_str.encode()).hexdigest().upper()
