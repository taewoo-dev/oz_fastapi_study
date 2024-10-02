from fastapi import APIRouter, Path, status, Depends

from core.authenticate.dtos.responses import JwtTokenResponseDto
from users.dtos.responses import UserResponseDto
from users.dtos.requests import (
    UserCreateRequestDto,
    UserUpdateRequestDto,
    UserSignInRequestDto,
    UserOtpRequestDto,
)
from users.domains.user import User
from core.authenticate.services.authenticate_service import AuthenticateService
from users.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

# CRUD


@router.get(
    "/",
    response_model=list[UserResponseDto],
    description="유저 리스트를 반환하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_users_handler(
    user_service: UserService = Depends(),
):
    users: User | None = user_service.get_all_users()
    return [UserResponseDto.build(user=user) for user in users]


@router.get(
    "/{user_id}",
    response_model=UserResponseDto,
    description="단일 유저를 반환하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_user_handler(
    user_id: int = Path(default=..., ge=1),
    _: str = Depends(AuthenticateService.get_username),
    user_service: UserService = Depends(),
):
    user: User | None = user_service.get_user_or_404_by_user_id(user_id=user_id)

    return UserResponseDto.build(user=user)


@router.get(
    "/me/",
    response_model=UserResponseDto,
    description="사용자 자신의 프로필을 조회하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_me_handler(
    username: str = Depends(AuthenticateService.get_username),
    user_service: UserService = Depends(),
):
    user: User | None = user_service.get_user_or_404_by_username(username=username)

    return UserResponseDto.build(user=user)


@router.patch(
    "/me/",
    response_model=UserResponseDto,
    description="유저 자신의 정보를 업데이트 하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def update_me_handler(
    body: UserUpdateRequestDto,
    username: str = Depends(AuthenticateService.get_username),
    user_service: UserService = Depends(),
):
    user: User | None = user_service.update_user_password_or_404(
        username=username,
        password=body.password,
    )

    return UserResponseDto.build(user=user)


@router.delete(
    "/me/",
    description="나의 계정을 삭제하는 API입니다",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_me_handler(
    username: str = Depends(AuthenticateService.get_username),
    user_service: UserService = Depends(),
):
    user_service.delete_user_or_404(username=username)


@router.post(
    "/sign-up",
    response_model=UserResponseDto,
    description="유저 회원가입 API입니다",
    status_code=status.HTTP_201_CREATED,
)
def user_sign_up_handler(
    body: UserCreateRequestDto,
    user_service: UserService = Depends(),
):
    new_user = user_service.create_user(username=body.username, password=body.password)

    return UserResponseDto.build(user=new_user)


@router.post(
    "/sign-in",
    response_model=JwtTokenResponseDto,
    description="유저 로그인 API입니다",
    status_code=status.HTTP_200_OK,
)
def user_sign_in_handler(
    body: UserSignInRequestDto,
    user_service: UserService = Depends(),
):
    access_token, refresh_token = user_service.authenticate_user_or_404(
        username=body.username, password=body.password
    )
    return JwtTokenResponseDto.build(
        access_token=access_token, refresh_token=refresh_token
    )


@router.post(
    "/email/otp",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
def send_otp_handler(
    body: UserOtpRequestDto,
    user_service: UserService = Depends(),
) -> None:
    user_service.validate_user_email_or_404(email=body.email)
    return
