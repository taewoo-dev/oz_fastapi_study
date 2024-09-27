import re
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from core.database.orm import Base


class User(Base):
    __tablename__ = "service_users"

    id = Column(Integer, primary_key=True)
    username = Column(String(16))  # Varchar 16
    password = Column(String(60))  # Bcrypt 60자
    created_at = Column(DateTime, default=datetime.now)

    @staticmethod
    def _validate_passowrd(password_hash: str) -> None:
        bcrypt_pattern = r"^\$2[aby]\$[0-9]{2}\$[./A-Za-z0-9]{53}$"
        assert re.match(bcrypt_pattern, password_hash) is not None

    @classmethod
    def create(cls, username: str, password: str):
        cls._validate_passowrd(password_hash=password)
        return cls(username=username, password=password)

    def update_password(self, new_password: str) -> None:
        self._validate_passowrd(password_hash=new_password)
        self.password = new_password
