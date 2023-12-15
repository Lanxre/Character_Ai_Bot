from bot import telegram_bot
from logger import FastApiAuthLogger

logger = FastApiAuthLogger("Telegram Shutdown")


async def on_shutdown():
	logger.info("Shutting...")
	await telegram_bot.session.close()
