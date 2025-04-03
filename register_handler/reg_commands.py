from aiogram import Dispatcher
from aiogram.filters import Command

from handler.commands import cmd_start, admin_cmd, cmd_about


async def register_handlers_commands(dp: Dispatcher):
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(admin_cmd, Command('admin'))
    dp.message.register(cmd_about, Command('about'))
