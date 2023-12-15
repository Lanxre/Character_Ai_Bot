from bot import telegram_bot, telegram_dispatcher
from bot.handlers.commands import bot_commands, command_router
from config import webhooks_settings
from logger import FastApiAuthLogger

logger = FastApiAuthLogger("Telegram StartUp")


async def on_startup():
	logger.info("Starting Telegram Bot")
	await telegram_bot.set_webhook(url=webhooks_settings.url)
	await telegram_bot.set_my_commands(commands=bot_commands)
	telegram_dispatcher.include_router(router=command_router)
