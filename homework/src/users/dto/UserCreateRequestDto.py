from pydantic import BaseModel


class UserCreateRequestDto(BaseModel):
    username: str
    password: str
