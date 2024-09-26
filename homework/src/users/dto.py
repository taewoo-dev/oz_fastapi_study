from datetime import datetime

from pydantic import BaseModel

from users.models import User


class UserSignInRequestDto(BaseModel):
    username: str
    password: str


class UserCreateRequestDto(BaseModel):
    username: str
    password: str


class UserUpdateRequestDto(BaseModel):
    password: str | None


# 팩토리 디자인
class UserResponseDto(BaseModel):
    id: int
    username: str
    created_at: datetime

    @classmethod
    def build(cls, user: User):
        return cls(id=user.id, username=user.username, created_at=user.created_at)
