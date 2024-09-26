from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from core.database.connection import get_db
from core.database.connection_async import get_async_db
from users.models import User


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def save(self, user: User):
        self.db.add(user)
        self.db.commit()

    def get_users(self) -> User | None:
        return self.db.query(User).all()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def delete(self, user: User):
        self.db.delete(user)
        self.db.commit()


class UserAsyncRepository:
    def __init__(self, db: AsyncSession = Depends(get_async_db)):
        self.db = db

    async def save(self, user: User) -> None:
        self.db.add(user)
        await self.db.commit()

    async def get_users(self) -> User | None:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.db.execute(
            select(User).filter(User.username == username),
        )
        return result.scalars().first()

    async def get_user_by_id(self, user_id) -> User | None:
        result = await self.db.execute(
            select(User).filter(User.id == user_id),
        )
        return result.scalars().first()

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()
