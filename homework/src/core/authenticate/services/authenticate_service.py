import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPBasic,
    HTTPAuthorizationCredentials,
    HTTPBearer,
    APIKeyHeader,
)
import time
import jwt

from core.authenticate.constants import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    JWT_EXPIRY_SECONDS,
    JWT_REFRESH_EXPIRY_SECONDS,
)
from core.authenticate.dtos.responses import JwtPayloadTypedDict

basic_auth = HTTPBasic()


class AuthenticateService:
    @staticmethod
    def hash_password(plain_password: str):
        plain_password_bytes = plain_password.encode("UTF-8")
        hashed_password = bcrypt.hashpw(plain_password_bytes, bcrypt.gensalt())
        return hashed_password.decode("UTF-8")

    @staticmethod
    def check_password(input_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            input_password.encode("UTF-8"),
            hashed_password.encode("UTF-8"),
        )

    @staticmethod
    def create_access_token(username: str) -> str:
        payload: JwtPayloadTypedDict = {
            "username": username,
            "isa": time.time(),
            "iss": "oz-coding",
        }
        return jwt.encode(
            payload=payload,
            key=JWT_SECRET_KEY,
            algorithm=JWT_ALGORITHM,
        )

    @staticmethod
    def create_refresh_token(username: str) -> str:
        payload: JwtPayloadTypedDict = {
            "username": username,
            "isa": time.time(),
            "iss": "oz-coding",
        }
        return jwt.encode(
            payload=payload,
            key=JWT_SECRET_KEY,
            algorithm=JWT_ALGORITHM,
        )

    @staticmethod
    def _decode_token(token: JwtPayloadTypedDict) -> dict:
        return jwt.decode(
            jwt=token,
            key=JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

    @staticmethod
    def is_valid_access_token(payload: JwtPayloadTypedDict) -> bool:
        return time.time() < payload["isa"] + JWT_EXPIRY_SECONDS

    @staticmethod
    def is_valid_refresh_token(payload: JwtPayloadTypedDict) -> bool:
        return time.time() < payload["isa"] + JWT_REFRESH_EXPIRY_SECONDS

    @staticmethod
    def _get_access_jwt(
        auth_header: HTTPAuthorizationCredentials = HTTPBearer(auto_error=False),
    ):
        if auth_header is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="JWT access not provided",
            )
        return auth_header.credentials

    @staticmethod
    def _get_refresh_jwt(
        auth_header: HTTPAuthorizationCredentials | None = APIKeyHeader(
            name="X-Refresh-Token", auto_error=False
        ),
    ):
        if auth_header is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="JWT refresh not provided",
            )
        return auth_header

    @staticmethod
    def get_username(
        access_token_in_header: HTTPAuthorizationCredentials = Depends(
            HTTPBearer(auto_error=False)
        ),
        refresh_token_in_header: str | None = Depends(
            APIKeyHeader(name="X-Refresh-Token", auto_error=False)
        ),
    ):
        access_token = AuthenticateService._get_access_jwt(access_token_in_header)
        access_token_payload = AuthenticateService._decode_token(access_token)

        refresh_token = AuthenticateService._get_refresh_jwt(refresh_token_in_header)
        refresh_token_payload = AuthenticateService._decode_token(refresh_token)

        if not AuthenticateService.is_valid_access_token(
            access_token_payload
        ) and not AuthenticateService.is_valid_refresh_token(refresh_token_payload):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired"
            )
        return access_token_payload.get("username")
