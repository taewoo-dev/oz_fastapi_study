from pydantic import BaseModel


class UserUpdateRequestDto(BaseModel):
    password: str | None
