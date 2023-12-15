from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.database.models import Character
from core.infrastructure.database.repo import BaseRepo


class CharactersRepo(BaseRepo):
	def __init__(self, session: AsyncSession):
		super().__init__(session)

	async def create(self, model_instance: Character) -> None:
		if not await self.exists(id=model_instance.id):
			self.session.add(model_instance)
			await self.session.commit()

	async def get(self, character_id: int) -> Optional[Character]:
		result = await self.session.execute(select(Character).filter_by(id=character_id))
		await self.session.close()
		return result.scalar()

	async def get_by_name(self, character_name: str) -> Optional[Character]:
		result = await self.session.execute(select(Character).filter_by(name=character_name))
		return result.scalar()

	async def get_all(self) -> List[Character]:
		result = await self.session.execute(select(Character))
		await self.session.close()
		return [model for model in result.scalars().all()]

	async def update(self, model_instance) -> None:
		async with self.session.begin():
			await self.session.merge(model_instance)

	async def delete(self, model_instance) -> None:
		async with self.session.begin():
			await self.session.delete(model_instance)

	async def exists(self, **kwargs):
		query = select(Character).filter_by(**kwargs)
		result = await self.session.execute(query)
		return result.scalar() is not None
