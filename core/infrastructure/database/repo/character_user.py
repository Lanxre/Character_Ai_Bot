from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.database.models import CharacterUser
from core.infrastructure.database.repo import BaseRepo


class CharacterUsersRepo(BaseRepo):
	def __init__(self, session: AsyncSession):
		super().__init__(session)

	async def create(self, model_instance) -> None:
		try:
			async with self.session.begin():
				is_exists = await self.exists(user_id=model_instance.user_id)
				print(is_exists)
				if is_exists:
					return

				self.session.add(model_instance)
				await self.session.flush()

		except SQLAlchemyError as e:
			error = str(e)
			await self.session.rollback()
			raise RuntimeError(error) from e
		finally:
			await self.session.close()



	async def get(self, user_id: int) -> Optional[CharacterUser]:
		result = await self.session.execute(select(CharacterUser).filter_by(user_id=user_id))
		return result.scalar()

	async def get_all(self) -> List[CharacterUser]:
		result = await self.session.execute(select(CharacterUser))
		await self.session.close()
		return [model for model in result.scalars().all()]

	async def update(self, model_instance) -> None:
		async with self.session.begin():
			await self.session.merge(model_instance)
			await self.session.commit()

	async def delete(self, model_instance) -> None:
		async with self.session.begin():
			await self.session.delete(model_instance)
			await self.session.commit()

	async def delete_by_user_id(self, user_id: int) -> None:
		is_exist = await self.exists(user_id=user_id)
		if is_exist:
			query = delete(CharacterUser).where(CharacterUser.user_id == user_id)
			await self.session.execute(query)
			await self.session.commit()

	async def exists(self, **kwargs):
		query = select(CharacterUser).filter_by(**kwargs)
		result = await self.session.execute(query)
		await self.session.close()
		return result.scalar() is not None

	async def close(self) -> None:
		await self.session.close()
