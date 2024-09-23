from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    id: int
    username: str


class UpdateUserRequest(BaseModel):
    username: str


class UserResponse(BaseModel):
    username: str


class UsersListResponse(BaseModel):
    users: list[UserResponse]


class CreateUserResponse(BaseModel):
    message: str


class UpdateUserResponse(BaseModel):
    message: str
