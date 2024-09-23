from fastapi import APIRouter, Path

users = [
    {"id": 1, "username": "hong1"},
    {"id": 2, "username": "hong2"},
    {"id": 3, "username": "hong3"},
]

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users_handler():
    return users


@router.get("/{user_id}")
def get_user_handler(user_id: int = Path(default=..., ge=1)):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"message": "User not found"}
