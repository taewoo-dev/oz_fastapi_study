from pydantic import BaseModel


class UserSignInRequestDto(BaseModel):
    username: str
    password: str
