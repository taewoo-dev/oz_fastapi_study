from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from .request import CreateUserRequest, UpdateUserRequest

router = APIRouter(prefix="/users", tags=["Users"])


users = []


@router.get("/")
def get_users_handler():
    return users


basic_auth = HTTPBasic()


@router.get("/me")
def get_me_handler(
    credentials: HTTPBasicCredentials = Depends(basic_auth),
):
    print(credentials.username, credentials.password)
    return


@router.post("/")
def create_user_handler(body: CreateUserRequest):
    new_user = {
        "id": body.id,
        "username": body.username,
    }
    users.append(new_user)
    return new_user


@router.get("/{username}")
def get_user(username: str):
    for user in users:
        if user["username"] == username:
            return user
    return {"message": "User not found"}


# PUT은 모든걸 덮어쓰기, PATCH는 일부분만 수정
@router.put("/{user_id}")
def replace_user_handler(user_id: int, body: UpdateUserRequest):
    for user in users:
        if user["id"] == user_id:
            user["username"] = body.username
            return user


@router.patch("/{user_id}")
def update_user_handler(user_id: int, body: UpdateUserRequest):
    for user in users:
        if user["id"] == user_id:
            user["username"] = body.username
            return user

    return {"message": "User not found"}


@router.delete("/{user_id}")
def delete_user_handler(user_id: int):
    for user in users:
        if user["user_id"] == user_id:
            users.remove(user)
            return {"message": "user is deleted"}

    return {"message": "User not found"}
