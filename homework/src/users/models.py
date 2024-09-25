from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from core.database.orm import Base


class User(Base):
    __tablename__ = "service_users"

    id = Column(Integer, primary_key=True)
    username = Column(String(16))  # Varchar 16
    password = Column(String(60))  # Bcrypt 60자
    created_at = Column(DateTime, default=datetime.now)

    @classmethod
    def create(cls, username: str, password: str):
        return cls(username=username, password=password)
