from aiogram.types import BotCommand


async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота!"),
        BotCommand(command="/about", description="Информация о компании"),
    ]
    await bot.set_my_commands(commands)
