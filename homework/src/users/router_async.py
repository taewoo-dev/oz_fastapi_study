from fastapi import APIRouter, Path, status, Depends, BackgroundTasks


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
from users.services import UserAsyncService

router = APIRouter(prefix="/async/users", tags=["Async Users"])

# CRUD


@router.get(
    "/",
    response_model=list[UserResponseDto],
    description="유저 리스트를 반환하는 API입니다",
    status_code=status.HTTP_200_OK,
)
async def get_users_handler(
    user_service: UserAsyncService = Depends(),
):
    users: User | None = await user_service.get_all_users()

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
    user_service: UserAsyncService = Depends(),
):
    user: User | None = await user_service.get_user_or_404_by_user_id(user_id=user_id)

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
    user_service: UserAsyncService = Depends(),
):
    user: User | None = await user_service.get_user_or_404_by_username(
        username=username
    )

    return UserResponseDto.build(user=user)


@router.patch(
    "/me/",
    response_model=UserResponseDto,
    description="유저 자신의 정보를 업데이트 하는 API입니다",
    status_code=status.HTTP_200_OK,
)
async def update_me_handler(
    body: UserUpdateRequestDto,
    username: str = Depends(AuthenticateService.get_username),
    user_service: UserAsyncService = Depends(),
):
    user: User | None = await user_service.update_user_password_or_404(
        username=username, password=body.password
    )

    return UserResponseDto.build(user=user)


@router.delete(
    "/me/",
    description="나의 계정을 삭제하는 API입니다",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_me_handler(
    username: str = Depends(AuthenticateService.get_username),
    user_service: UserAsyncService = Depends(),
):
    user: User | None = await user_service.delete_user_or_404(username=username)


@router.post(
    "/sign-up",
    response_model=UserResponseDto,
    description="유저 회원가입 API입니다",
)
async def user_sign_up_handler(
    body: UserCreateRequestDto,
    background_task: BackgroundTasks,
    user_service: UserAsyncService = Depends(),
):
    new_user = await user_service.create_user(
        username=body.username, password=body.password
    )

    background_task.add_task(send_email, "회원가입을 축하합니다!")

    return UserResponseDto.build(user=new_user)


@router.post(
    "/sign-in",
    response_model=JwtTokenResponseDto,
    description="유저 로그인 API입니다",
)
async def user_sign_in_handler(
    body: UserSignInRequestDto,
    user_service: UserAsyncService = Depends(),
):
    access_token = await user_service.authenticate_user_or_404(
        username=body.username, password=body.password
    )

    return JwtTokenResponseDto.build(access_token=access_token)
