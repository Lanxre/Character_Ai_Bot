from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import telegram_settings, database_settings
from core.infrastructure.database import DatabaseManager

storage = MemoryStorage()
bot = Bot(token=telegram_settings.bot_token, parse_mode=ParseMode.HTML)
db_manager = DatabaseManager(database_settings)
dp = Dispatcher(storage=storage)
