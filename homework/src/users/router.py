from fastapi import APIRouter, Path, status, HTTPException

from users.dto import (
    CreateUserRequest,
    UpdateUserRequest,
    UsersListResponse,
    UserResponse,
    CreateUserResponse,
    UpdateUserResponse,
)

users = [
    {"id": 1, "username": "hong1"},
    {"id": 2, "username": "hong2"},
    {"id": 3, "username": "hong3"},
]

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=UsersListResponse,
    description="유저 리스트를 반환하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_users_handler():
    return UsersListResponse(users=users)


@router.post(
    "/",
    response_model=CreateUserResponse,
    description="단일 유저를 생성하는 API입니다",
    status_code=status.HTTP_201_CREATED,
)
def create_user_handler(body: CreateUserRequest):
    users.append(
        {
            "id": body.id,
            "username": body.username,
        }
    )
    return CreateUserResponse(message="user is created")


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    description="단일 유저를 반환하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_user_handler(user_id: int = Path(default=..., ge=1)):
    for user in users:
        if user["id"] == user_id:
            return UserResponse(username=user["username"])
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


@router.patch(
    "/{user_id}",
    response_model=UpdateUserResponse,
    description="단일 유저를 정보를 업데이트 하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def update_user(user_id: int, body: UpdateUserRequest):
    for user in users:
        if user["id"] == user_id:
            user["username"] = body.username
            return UpdateUserResponse(message="유저 데이터를 성공적으로 변경했습니다")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


@router.delete(
    "/{user_id}",
    description="단일 유저를 삭제하는 API입니다",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )
