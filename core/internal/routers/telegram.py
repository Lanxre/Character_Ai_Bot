from typing import List
from urllib.parse import parse_qsl

from aiogram.types import Update
from aiogram.utils.web_app import safe_parse_webapp_init_data
from amplitude import BaseEvent
from fastapi import APIRouter, Depends
from fastapi import Request
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from bot import telegram_dispatcher, telegram_bot
from config import webhooks_settings, WEB_DIR, telegram_settings
from core.configuration.amplitude_client import amplitude_client
from core.infrastructure.database.models import CharacterUser, Character
from core.infrastructure.database.repo import RequestsRepo
from core.infrastructure.database.setup import db_manager

router = APIRouter(tags=["Telegram"])
templates = Jinja2Templates(directory=WEB_DIR)


@router.post(webhooks_settings.path)
async def telegram_bot_webhook(update: dict):
	telegram_update = Update(**update)
	await telegram_dispatcher.feed_update(bot=telegram_bot, update=telegram_update)


@router.get("/character")
async def telegram_bot_chat(
		request: Request,
		repo: RequestsRepo = Depends(db_manager.get_repo)
):
	characters: List[Character] = await repo.characters.get_all()
	return templates.TemplateResponse("demo.html", {"request": request,
	                                                "characters": characters})


@router.post("/character")
async def telegram_bot_chat(
		request: Request
):
	try:
		data = await request.body()
		parsed_data = dict(parse_qsl(data.decode("utf-8")))
		web_app_init_data = safe_parse_webapp_init_data(
			token=telegram_settings.bot_token,
			init_data=parsed_data["_auth"]
		)

		amplitude_client.track(
			BaseEvent(
				event_type="User chosen character",
				user_id=f"{web_app_init_data.user.id}"
			)
		)

		repository = await db_manager.get_repo()

		is_exist = await repository.character_user.exists(user_id=web_app_init_data.user.id)
		if is_exist:
			await telegram_bot.send_message(chat_id=web_app_init_data.user.id,
			                                text=f"Ты уже выбрал персонажа. Заверши диалог /end и начни новый ")

			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="You have already selected a character. Finish the dialogue (/end) and start a new one."
			)

		# session problem == fix
		cu = CharacterUser(
			user_id=web_app_init_data.user.id,
			character_id=parsed_data['character_id']
		)

		d = db_manager.create_session_pool()
		async with d.begin() as s:
			s.add(cu)
			await s.commit()
			await s.close()

		# await repository.character_user.create(q)

		character = await repository.characters.get(character_id=parsed_data['character_id'])



		await telegram_bot.send_message(
			chat_id=web_app_init_data.user.id,
			text=f"Ты выбрал: {character.name}, {character.type}"
		)

		await telegram_bot.send_message(
			chat_id=web_app_init_data.user.id,
			text=f"{character.name}: {character.greeted_message}"
		)

		return JSONResponse(status_code=status.HTTP_200_OK,
		                    content={"character_id": web_app_init_data.query_id})
	except Exception as e:
		return HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"An error occurred: {str(e)}"
		)
