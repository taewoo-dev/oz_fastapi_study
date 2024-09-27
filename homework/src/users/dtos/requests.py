from pydantic import BaseModel


class UserCreateRequestDto(BaseModel):
    username: str
    password: str


class UserSignInRequestDto(BaseModel):
    username: str
    password: str


class UserUpdateRequestDto(BaseModel):
    password: str | None
