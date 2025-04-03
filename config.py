from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN="7940506524:AAGFUwd8RcwBUrRmf52q_1g5R6viSIe4QIs"
BD="sqlite:///database.db"
ADMIN_ID="1028962949"
ROBOKASSA_LOGIN = "barketing"
ROBOKASSA_PASS1 = "Q7NPQkbk2q2qojGoeN38"
ROBOKASSA_PASS2 = "WOg5mSXJGF6BQe0KS72t"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
