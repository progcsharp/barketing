from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN="7940506524:AAGFUwd8RcwBUrRmf52q_1g5R6viSIe4QIs"
BD="sqlite:///database.db"
ADMIN_ID="1028962949"
ROBOKASSA_LOGIN = "barketing"
ROBOKASSA_PASS1 = "u0WdyxxI4JkMk1k3j5hK"
ROBOKASSA_PASS2 = "DZ2D1T9mTvIgQgLd7Vx6"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
