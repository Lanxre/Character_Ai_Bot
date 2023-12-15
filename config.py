from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseSettings):
	model_config = SettingsConfigDict(env_prefix="TELEGRAM_", env_file="./.env")

	bot_token: str


class ServerSettings(BaseSettings):
	model_config = SettingsConfigDict(env_prefix="SERVER_", env_file="./.env")

	server_create_path: str = 'main:create_app'

	host: str
	port: int


class WebHooksSettings(BaseSettings):
	model_config = SettingsConfigDict(env_prefix='WEBHOOK_', env_file="./.env")

	ngrock_tunnel_url: str
	path: str
	url: str


class DatabaseSettings(BaseSettings):
	model_config = SettingsConfigDict(env_prefix='DATABASE_', env_file="./.env")

	name: str

	def construct_sqlalchemy_url(self) -> str:
		return f"sqlite+aiosqlite:///{self.name}"


WORK_DIR = Path(__file__).parent
WEB_DIR = Path(__file__).parent / 'front'



server_settings = ServerSettings()
telegram_settings = TelegramSettings()
webhooks_settings = WebHooksSettings()
database_settings = DatabaseSettings()