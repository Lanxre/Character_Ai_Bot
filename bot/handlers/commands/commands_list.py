from typing import List

from aiogram.types import BotCommand

bot_commands: List[BotCommand] = [
	BotCommand(command="/start", description="Главное меню бота"),
	BotCommand(command="/menu", description="Меню персонажей"),
	BotCommand(command="/end", description="Завершить чат с персонажем"),
	BotCommand(command="/delete", description="Удалить сообщения"),
]
