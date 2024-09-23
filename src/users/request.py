from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    id: int
    username: str


class UpdateUserRequest(BaseModel):
    username: str | None = None
