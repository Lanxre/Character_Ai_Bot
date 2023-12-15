from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from core.configuration.routers import __routers__
from core.internal.events import on_startup, on_shutdown


class Server:
	__app: FastAPI

	def __init__(self, app: FastAPI):
		self.__app = app
		self.__register_routes(app)
		self.__register_events(app)

	def get_app(self) -> FastAPI:
		return self.__app

	@staticmethod
	def __static_files(app: FastAPI) -> None:
		app.mount("/static", StaticFiles(directory="front"), name="static")


	@staticmethod
	def __register_routes(app: FastAPI) -> None:
		__routers__.register_routes(app)

	@staticmethod
	def __register_events(app: FastAPI) -> None:
		app.on_event('startup')(on_startup)
		app.on_event('shutdown')(on_shutdown)
