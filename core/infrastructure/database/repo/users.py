from typing import Type, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.database.models import User
from core.infrastructure.database.repo import BaseRepo


class UsersRepo(BaseRepo):
	def __init__(self, session: AsyncSession):
		super().__init__(session)

	async def create(self, model_instance) -> None:
		async with self.session.begin():
			is_exists = await self.exists(User, username=model_instance.username)
			if not is_exists:
				self.session.add(model_instance)

		await self.session.close()

	async def get(self, primary_key: int) -> Optional[Type]:
		result = await self.session.execute(select(User).filter_by(id=primary_key))
		return result.scalar()

	async def get_all(self) -> List[User]:
		result = await self.session.execute(select(User))
		return [user for user in result.scalars().all()]

	async def update(self, model_instance) -> None:
		async with self.session.begin():
			await self.session.merge(model_instance)

	async def delete(self, model_instance) -> None:
		async with self.session.begin():
			await self.session.delete(model_instance)

	async def exists(self, model, **kwargs):
		query = select(model).filter_by(**kwargs)
		result = await self.session.execute(query)
		return result.scalar() is not None