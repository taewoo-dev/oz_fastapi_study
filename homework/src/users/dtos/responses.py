from datetime import datetime

from pydantic import BaseModel

from users.domains.user import User


class UserResponseDto(BaseModel):
    id: int
    username: str
    created_at: datetime

    @classmethod
    def build(cls, user: User):
        return cls(id=user.id, username=user.username, created_at=user.created_at)
