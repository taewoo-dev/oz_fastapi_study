from fastapi import Depends
from sqlalchemy.orm import Session

from core.database.connection import get_db
from users.domain.User import User


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
