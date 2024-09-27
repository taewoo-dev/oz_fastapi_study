from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.connection_async import get_async_db
from users.domains.user import User


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
