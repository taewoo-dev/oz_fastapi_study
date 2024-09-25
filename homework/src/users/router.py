from fastapi import APIRouter, Path, status, HTTPException, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqlalchemy.orm import Session

from core.authenticate.dto import JwtTokenResponseDto
from core.database.connection import get_db
from users.dto import (
    UserResponseDto,
    UserCreateRequestDto,
    UserUpdateRequestDto,
    UserSignInRequestDto,
)
from users.models import User
from core.authenticate.services import AuthenticateService

users = [
    {"id": 1, "username": "hong1", "password": "pw1"},
    {"id": 2, "username": "hong2", "password": "pw2"},
    {"id": 3, "username": "hong3", "password": "pw3"},
]

router = APIRouter(prefix="/users", tags=["Users"])

# CRUD


@router.get(
    "/",
    response_model=list[UserResponseDto],
    description="유저 리스트를 반환하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_users_handler():
    return [UserResponseDto.build(user=user) for user in users]


@router.post(
    "/",
    response_model=UserResponseDto,
    description="단일 유저를 생성하는 API입니다",
    status_code=status.HTTP_201_CREATED,
)
def create_user_handler(
    body: UserCreateRequestDto,
    auth_service: AuthenticateService = Depends(AuthenticateService),
    db: Session = Depends(get_db),
):
    new_user = User.create(
        username=body.username,
        password=auth_service.hash_password(plain_password=body.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponseDto.build(user=new_user)


@router.get(
    "/{user_id}",
    response_model=UserResponseDto,
    description="단일 유저를 반환하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_user_handler(user_id: int = Path(default=..., ge=1)):
    for user in users:
        if user["id"] == user_id:
            return UserResponseDto.build(user=user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


@router.patch(
    "/{user_id}",
    response_model=UserResponseDto,
    description="단일 유저를 정보를 업데이트 하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def update_user(user_id: int, body: UserUpdateRequestDto):
    for user in users:
        if user["id"] == user_id:
            if body.username:
                user["username"] = body.username
            if body.password:
                user["password"] = body.password
            return UserResponseDto.build(user=user)
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
            return None
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


# Basic Authenticate
@router.get(
    "/me/",
    response_model=UserResponseDto,
    description="사용자 자신의 프로필을 조회하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_me_handler(
    username: str = Depends(AuthenticateService.get_username),
    db: Session = Depends(get_db),
):
    user: User | None = db.query(User).filter(User.username == username).first()

    if user:
        return UserResponseDto.build(user=user)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )


# JWT Authenticate
@router.post(
    "/sign-up",
    response_model=UserResponseDto,
    description="유저 회원가입 API입니다",
)
def user_sign_up_handler(
    body: UserCreateRequestDto,
    auth_service: AuthenticateService = Depends(AuthenticateService),
    db: Session = Depends(get_db),
):
    new_user = User.create(
        username=body.username,
        password=auth_service.hash_password(plain_password=body.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponseDto.build(user=new_user)


@router.post(
    "/sign-in",
    response_model=JwtTokenResponseDto,
    description="유저 로그인 API입니다",
)
def user_sign_in_handler(
    body: UserSignInRequestDto,
    authenticate_service: AuthenticateService = Depends(AuthenticateService),
    db: Session = Depends(get_db),
):
    user: User | None = db.query(User).filter(User.username == body.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    access_token = authenticate_service.create_access_token(user.username)

    return JwtTokenResponseDto.build(access_token=access_token)


# 2-6 jwt 토큰 발행 후 로그인 까지 해야함
