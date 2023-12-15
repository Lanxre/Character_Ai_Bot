from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.database.models import TelegramMessage
from core.infrastructure.database.repo import BaseRepo


class TelegraMessagesRepo(BaseRepo):
	def __init__(self, session: AsyncSession):
		super().__init__(session)

	async def create(self, model_instance) -> None:
		async with self.session.begin():
			is_exists = await self.exists(TelegramMessage, id=model_instance.id)
			if not is_exists:
				self.session.add(model_instance)

	async def get(self, primary_key: int) -> Optional[TelegramMessage]:
		result = await self.session.execute(select(TelegramMessage).filter_by(id=primary_key))
		return result.scalar()

	async def get_all(self) -> List[TelegramMessage]:
		result = await self.session.execute(select(TelegramMessage))
		return [model for model in result.scalars().all()]

	async def update(self, model_instance) -> None:
		async with self.session.begin():
			await self.session.merge(model_instance)

	async def delete(self, model_instance) -> None:
		async with self.session.begin():
			await self.session.delete(model_instance)

	async def delete_by_user_id(self, user_id: int) -> None:
		query = delete(TelegramMessage).where(TelegramMessage.user_id == user_id)
		await self.session.execute(query)
		await self.session.commit()

	async def exists(self, model, **kwargs):
		query = select(model).filter_by(**kwargs)
		result = await self.session.execute(query)
		return result.scalar() is not None
