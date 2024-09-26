from fastapi import APIRouter, Path, status, HTTPException, Depends

from core.authenticate.dto import JwtTokenResponseDto
from users.dto import (
    UserResponseDto,
    UserCreateRequestDto,
    UserUpdateRequestDto,
    UserSignInRequestDto,
)
from users.models import User
from core.authenticate.services import AuthenticateService
from users.repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])

# CRUD


@router.get(
    "/",
    response_model=list[UserResponseDto],
    description="유저 리스트를 반환하는 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_users_handler(
    user_repo: UserRepository = Depends(),
):
    users: User | None = user_repo.get_users()
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
    user_repo: UserRepository = Depends(),
):
    user: User | None = user_repo.get_user_by_id(user_id=user_id)

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
def get_me_handler(
    username: str = Depends(AuthenticateService.get_username),
    user_repo: UserRepository = Depends(),
):
    user: User | None = user_repo.get_user_by_username(username=username)

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
def update_me_handler(
    body: UserUpdateRequestDto,
    auth_service: AuthenticateService = Depends(),
    username: str = Depends(AuthenticateService.get_username),
    user_repo: UserRepository = Depends(),
):
    user: User | None = user_repo.get_user_by_username(username=username)

    if user:
        new_password = auth_service.hash_password(plain_password=body.password)
        user.update_password(new_password=new_password)
        user_repo.save(user)
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
def delete_me_handler(
    username: str = Depends(AuthenticateService.get_username),
    user_repo: UserRepository = Depends(),
):
    user: User | None = user_repo.get_user_by_username(username=username)

    if user:
        user_repo.delete(user)
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
def user_sign_up_handler(
    body: UserCreateRequestDto,
    auth_service: AuthenticateService = Depends(),
    user_repo: UserRepository = Depends(),
):
    new_user = User.create(
        username=body.username,
        password=auth_service.hash_password(plain_password=body.password),
    )

    user_repo.save(user=new_user)

    return UserResponseDto.build(user=new_user)


@router.post(
    "/sign-in",
    response_model=JwtTokenResponseDto,
    description="유저 로그인 API입니다",
)
def user_sign_in_handler(
    body: UserSignInRequestDto,
    authenticate_service: AuthenticateService = Depends(),
    user_repo: UserRepository = Depends(),
):
    user: User | None = user_repo.get_user_by_username(body.username)

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
