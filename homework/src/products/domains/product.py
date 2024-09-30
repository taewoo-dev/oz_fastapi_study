from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from core.database.orm import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(16))  # Varchar 16
    price = Column(Integer)  # Bcrypt 60자
    created_at = Column(DateTime, default=datetime.now)
