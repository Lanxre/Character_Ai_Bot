import asyncio

import uvicorn
from fastapi import FastAPI

from config import server_settings, database_settings
from core.configuration.server import Server
from core.infrastructure.database import DatabaseManager


def create_app() -> FastAPI:
	application = FastAPI()
	return Server(app=application).get_app()


async def main() -> None:
	database_manager = DatabaseManager(database_settings)
	await database_manager.init_models()
	uvicorn.run(
		app=server_settings.server_create_path,
		host=server_settings.host,
		port=server_settings.port,
		reload=True
	)


if __name__ == "__main__":
	asyncio.run(main())
