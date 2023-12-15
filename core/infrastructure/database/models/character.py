from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.infrastructure.database.models import BaseModel


class User(BaseModel):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	username: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=True)
	first_name: Mapped[str] = mapped_column(String)
	last_name: Mapped[str] = mapped_column(String, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

	messages = relationship('TelegramMessage', back_populates='user')
	character_users = relationship('CharacterUser', back_populates='user')


class Character(BaseModel):
	__tablename__ = "characters"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String)
	type: Mapped[str] = mapped_column(String)
	image_url: Mapped[str] = mapped_column(String)
	system_messages: Mapped[str] = mapped_column(Text)
	greeted_message: Mapped[str] = mapped_column(Text)

	messages = relationship('TelegramMessage', back_populates='character')
	character_users = relationship('CharacterUser', back_populates='character')



class TelegramMessage(BaseModel):
	__tablename__ = 'telegram_messages'

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	text: Mapped[str] = mapped_column(Text)
	timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, server_default=func.now())
	user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
	character_id: Mapped[int] = mapped_column(Integer, ForeignKey('characters.id'))

	user: Mapped[List[User]] = relationship('User', back_populates='messages')
	character: Mapped[List[Character]] = relationship('Character', back_populates='messages')


class CharacterUser(BaseModel):
	__tablename__ = "character_users"

	user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
	character_id: Mapped[int] = mapped_column(Integer, ForeignKey('characters.id'), primary_key=True)

	user: Mapped["User"] = relationship(back_populates='character_users')
	character: Mapped["Character"] = relationship(back_populates='character_users')