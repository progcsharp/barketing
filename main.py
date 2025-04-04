import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import bot
from keyboards.set_commands import set_commands
from register_handler.reg_callback import register_handlers_callback
from register_handler.reg_commands import register_handlers_commands
from register_handler.reg_message import register_handlers_message


async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    await set_commands(bot)

    await register_handlers_commands(dp)
    await register_handlers_callback(dp)
    await register_handlers_message(dp)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
