from fastapi import Depends

from core.authenticate.services.authenticate_service import AuthenticateService
from users.domains.user import User
from users.exceptions.custom_exceptions import (
    InvalidPasswordException,
    UserNotFoundException,
)
from users.repositorys.user_repository import UserRepository


# 의존 관계
# UserService <- UserRepository
# UserService <- AuthenticateService


class UserService:
    def __init__(
        self,
        repo: UserRepository = Depends(),
        auth_service: AuthenticateService = Depends(),
    ):
        self.user_repo = repo
        self.auth_service = auth_service

    def create_user(self, username: str, password: str) -> User:
        new_user = User.create(
            username=username,
            password=self.auth_service.hash_password(plain_password=password),
        )

        self.user_repo.save(user=new_user)

        return new_user

    def get_all_users(self) -> User | None:
        users = self.user_repo.get_users()

        self._validate_user_or_raise(user=users)

        return users

    def get_user_or_404_by_user_id(self, user_id: int) -> User:
        user: User | None = self.user_repo.get_user_by_id(user_id=user_id)

        self._validate_user_or_raise(user)

        return user

    def get_user_or_404_by_username(self, username: str) -> User:
        user: User | None = self.user_repo.get_user_by_username(username=username)

        self._validate_user_or_raise(user)

        return user

    def update_user_password_or_404(self, username: str, password: str) -> User:
        user: User | None = self.user_repo.get_user_by_username(username=username)

        self._validate_user_or_raise(user)

        new_password = self.auth_service.hash_password(plain_password=password)
        user.update_password(new_password=new_password)
        self.user_repo.save(user)

        return user

    def delete_user_or_404(self, username: str) -> None:
        user: User | None = self.user_repo.get_user_by_username(username=username)

        self._validate_user_or_raise(user)

        self.user_repo.delete(user)

    def authenticate_user_or_404(self, username: str, password: str) -> tuple[str, str]:
        user: User | None = self.user_repo.get_user_by_username(username=username)

        self._validate_user_or_raise(user)

        if not self.auth_service.check_password(
            input_password=password, hashed_password=user.password
        ):
            raise InvalidPasswordException()

        access_token = self.auth_service.create_access_token(user.username)
        refresh_token = self.auth_service.create_refresh_token(user.username)

        return access_token, refresh_token

    @staticmethod
    def _validate_user_or_raise(user: User | None) -> None:
        if user is None:
            raise UserNotFoundException()
