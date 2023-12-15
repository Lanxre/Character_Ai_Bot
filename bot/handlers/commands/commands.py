from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, WebAppInfo, MenuButtonWebApp, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.utils.markdown import hbold, hlink
from amplitude import BaseEvent

from bot import db_manager, telegram_bot
from config import webhooks_settings
from core.configuration.amplitude_client import amplitude_client
from core.infrastructure.database.models import User, TelegramMessage
from core.internal.external.fetch import fetch_completion
from logger import TelegramLogger, LogLevel
from ..constants import IMAGE_COMMANDS

command_router = Router()

logger = TelegramLogger(logger_name="TgHandler", level=LogLevel.DEBUG)


@command_router.message(CommandStart())
async def start_handler(message: Message) -> None:
	try:
		user = User(
			id=message.from_user.id,
			username=message.from_user.username,
			first_name=message.from_user.first_name,
			last_name=message.from_user.last_name,
		)
		amplitude_client.track(
			BaseEvent(
				event_type="Register",
				user_id=f"{message.from_user.id}"
			)
		)

		repository = await db_manager.get_repo()
		await repository.users.create(user)

		await telegram_bot.set_chat_menu_button(
			chat_id=message.chat.id,
			menu_button=MenuButtonWebApp(text="Меню",
			                             web_app=WebAppInfo(url=webhooks_settings.ngrock_tunnel_url + '/character')),
		)

		keyboard_builder = InlineKeyboardBuilder()
		keyboard_builder.add(InlineKeyboardButton(
			text="Выбрать персоанажа",
			web_app=WebAppInfo(url=webhooks_settings.ngrock_tunnel_url + '/character')
		))
		greeting_text = (f"👋 {hbold('Приветствую тебя, дорогой друг!')} 🌟\n\n"
		                 f"Я - бот,"
		                 f" интегрированный с {hlink(title='Character.AI', url='https://beta.character.ai/')}, "
		                 f"где ты можешь общаться с различными реальными и вымышленными персонажами. 💬🎭\n\n"
		                 f"🤖 {hbold('Вот мои основные команды при общении с персонажем:')}\n"
		                 "- 🌟 Кнопка для выбора персонажа /menu \n"
		                 "- 🚫 Завершить диалог с текущим персонажем, используй команду /end.\n"
		                 "- 🗑 Удалить всю переписку с персонажем, начать заново с помощью /delete.")

		await message.chat.bot.send_photo(
			chat_id=message.chat.id,
			photo=FSInputFile(path=IMAGE_COMMANDS.get("start")),
			caption=greeting_text,
			reply_markup=keyboard_builder.as_markup()
		)

	except Exception as e:
		logger.error(message="Start command", error=e)


@command_router.message(Command("delete"))
async def delete_messages(message: Message):
	try:
		repository = await db_manager.get_repo()
		await repository.messanger.delete_by_user_id(message.from_user.id)
		await message.answer(text="Ваш диалог с ботом был удалён!")
	except Exception as e:
		logger.error(message="Delete command", error=e)


@command_router.message(Command("end"))
async def stop_messages(message: Message):
	try:
		repository = await db_manager.get_repo()
		await repository.character_user.delete_by_user_id(message.from_user.id)
		await repository.character_user.close()
		await message.answer(text="Чат с персонажем завершен.")
	except Exception as e:
		logger.error(message="Stop command", error=e)


@command_router.message(Command("menu"))
async def command_webview(message: Message):
	await message.answer(
		text="Меню персонажей",
		reply_markup=InlineKeyboardMarkup(
			inline_keyboard=[
				[
					InlineKeyboardButton(
						text="Открыть", web_app=WebAppInfo(url=webhooks_settings.ngrock_tunnel_url + '/character')
					)
				]
			]
		),
	)


@command_router.message(F.text)
async def user_message(message: Message):
	try:
		repository = await db_manager.get_repo()
		is_exist = await repository.character_user.exists(user_id=message.from_user.id)
		if not is_exist:
			await message.answer('Ты не выбрал ещё своего персонажа!')
			return

		amplitude_client.track(
			BaseEvent(
				event_type="User send request",
				user_id=f"{message.from_user.user.id}"
			)
		)

		character_user = await repository.character_user.get(user_id=message.from_user.id)

		# session problem == fix
		tm = TelegramMessage(
			text=message.text,
			user_id=message.from_user.id,
			character_id=character_user.character_id
		)

		session = db_manager.create_session_pool()
		async with session.begin() as s:
			s.add(tm)
			await s.commit()
			await s.close()

		character = await repository.characters.get(character_id=character_user.character_id)

		character_message = await fetch_completion(
			system_message=character.system_messages,
			user_message=message.text
		)

		amplitude_client.track(
			BaseEvent(
				event_type="Answer from gpt",
				user_id=f"{message.from_user.user.id}"
			)
		)

		await message.answer(f"{character.name}: {character_message.content}")

		amplitude_client.track(
			BaseEvent(
				event_type="Bot send answer",
				user_id=f"{message.from_user.user.id}"
			)
		)

	except Exception as e:
		logger.error(message="Text handler", error=e)
