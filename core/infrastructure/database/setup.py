from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import scoped_session

from config import DatabaseSettings, database_settings
from core.infrastructure.database.models import BaseModel
from core.infrastructure.database.repo.requests import RequestsRepo


class DatabaseManager:
	def __init__(self, config: DatabaseSettings, echo=False):
		self.engine = self.create_engine(config, echo=echo)
		self.session_pool = self.create_session_pool()
		self.session_factory = scoped_session(self.session_pool)

	@staticmethod
	def create_engine(config: DatabaseSettings, echo=False) -> AsyncEngine:
		engine = create_async_engine(
			config.construct_sqlalchemy_url(),
			echo=echo,
		)

		return engine

	def create_session_pool(self) -> async_sessionmaker[AsyncSession]:
		session_pool = async_sessionmaker(bind=self.engine, expire_on_commit=False)
		return session_pool

	def get_session_db(self):
		session = self.session_factory()
		try:
			yield session
		except Exception as _:
			session.rollback()
			raise

	async def get_repo(self) -> RequestsRepo:
		# async with self.session_pool() as session:
		return RequestsRepo(next(self.get_session_db()))

	async def init_models(self) -> None:
		async with self.engine.begin() as conn:
			await conn.run_sync(BaseModel.metadata.create_all)


db_manager = DatabaseManager(database_settings)
