from fastapi import APIRouter, Path, status, HTTPException, Depends, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.authenticate.dto import JwtTokenResponseDto
from core.email import send_email
from users.dto import (
    UserResponseDto,
    UserCreateRequestDto,
    UserUpdateRequestDto,
    UserSignInRequestDto,
)
from users.models import User
from core.authenticate.services import AuthenticateService
from users.repository import UserAsyncRepository

router = APIRouter(prefix="/async/users", tags=["Async Users"])

# CRUD


@router.get(
    "/",
    response_model=list[UserResponseDto],
    description="유저 리스트를 반환하는 API입니다",
    status_code=status.HTTP_200_OK,
)
async def get_users_handler(
    user_repo: UserAsyncRepository = Depends(),
):
    users: User | None = await user_repo.get_users()
    print(users)
    return [UserResponseDto.build(user=user) for user in users]


@router.get(
    "/{user_id}",
    response_model=UserResponseDto,
    description="단일 유저를 반환하는 API입니다",
    status_code=status.HTTP_200_OK,
)
async def get_user_handler(
    user_id: int = Path(default=..., ge=1),
    _: str = Depends(AuthenticateService.get_username),
    user_repo: UserAsyncRepository = Depends(),
):
    user: User | None = await user_repo.get_user_by_id(user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserResponseDto.build(user=user)


# Basic Authenticate
@router.get(
    "/me/",
    response_model=UserResponseDto,
    description="사용자 자신의 프로필을 조회하는 API입니다",
    status_code=status.HTTP_200_OK,
)
async def get_me_handler(
    username: str = Depends(AuthenticateService.get_username),
    user_repo: UserAsyncRepository = Depends(),
):
    user: User | None = await user_repo.get_user_by_username(username=username)

    if user:
        return UserResponseDto.build(user=user)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )


@router.patch(
    "/me/",
    response_model=UserResponseDto,
    description="유저 자신의 정보를 업데이트 하는 API입니다",
    status_code=status.HTTP_200_OK,
)
async def update_me_handler(
    body: UserUpdateRequestDto,
    auth_service: AuthenticateService = Depends(),
    username: str = Depends(AuthenticateService.get_username),
    user_repo: UserAsyncRepository = Depends(),
):
    user: User | None = await user_repo.get_user_by_username(username=username)

    if user:
        new_password = auth_service.hash_password(plain_password=body.password)
        user.update_password(new_password=new_password)

        await user_repo.save(user=user)

        return UserResponseDto.build(user=user)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )


@router.delete(
    "/me/",
    description="나의 계정을 삭제하는 API입니다",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_me_handler(
    username: str = Depends(AuthenticateService.get_username),
    user_repo: UserAsyncRepository = Depends(),
):
    user: User | None = await user_repo.get_user_by_username(username=username)

    if user:
        await user_repo.delete(user=user)
        return None

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
async def user_sign_up_handler(
    body: UserCreateRequestDto,
    background_task: BackgroundTasks,
    auth_service: AuthenticateService = Depends(),
    user_repo: UserAsyncRepository = Depends(),
):
    new_user = User.create(
        username=body.username,
        password=auth_service.hash_password(plain_password=body.password),
    )

    await user_repo.save(user=new_user)

    background_task.add_task(send_email, "회원가입을 축하합니다!")

    return UserResponseDto.build(user=new_user)


@router.post(
    "/sign-in",
    response_model=JwtTokenResponseDto,
    description="유저 로그인 API입니다",
)
async def user_sign_in_handler(
    body: UserSignInRequestDto,
    authenticate_service: AuthenticateService = Depends(),
    user_repo: UserAsyncRepository = Depends(),
):
    # 비동기 방식은 두번에 나눠서 쿼리를 진행
    # 네트워크 IO가 발생하는 순간에 대기

    user: User | None = await user_repo.get_user_by_username(username=body.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not authenticate_service.check_password(
        input_password=body.password, hashed_password=user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    access_token = authenticate_service.create_access_token(user.username)

    return JwtTokenResponseDto.build(access_token=access_token)
