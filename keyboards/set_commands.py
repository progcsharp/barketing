from aiogram.types import BotCommand


async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота!"),
        BotCommand(command="/report_issue", description="Сообщить о проблеме."),
        BotCommand(command="/suggest", description="Предложить улучшение."),
        BotCommand(command="/open", description="Открыть приложение.")
    ]
    await bot.set_my_commands(commands)
