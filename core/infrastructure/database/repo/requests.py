from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.database.repo import UsersRepo, TelegraMessagesRepo, CharacterUsersRepo, CharactersRepo


@dataclass
class RequestsRepo:
	session: AsyncSession

	@property
	def users(self) -> UsersRepo:
		return UsersRepo(self.session)

	@property
	def characters(self) -> CharactersRepo:
		return CharactersRepo(self.session)

	@property
	def messanger(self) -> TelegraMessagesRepo:
		return TelegraMessagesRepo(self.session)

	@property
	def character_user(self) -> CharacterUsersRepo:
		return CharacterUsersRepo(self.session)
