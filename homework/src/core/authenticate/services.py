import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials, HTTPBearer
import time
import jwt

from core.authenticate.constants import (
    JWT_ALGORITHM,
    JWT_SECURITY_KEY,
    JWT_EXPIRY_SECONDS,
)
from core.authenticate.dto import JwtPayloadTypedDict

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
            key=JWT_SECURITY_KEY,
            algorithm=JWT_ALGORITHM,
        )

    @staticmethod
    def _decode_access_token(access_token: JwtPayloadTypedDict) -> dict:
        return jwt.decode(
            jwt=access_token,
            key=JWT_SECURITY_KEY,
            algorithms=[JWT_ALGORITHM],
        )

    @staticmethod
    def is_valid_token(payload: JwtPayloadTypedDict) -> bool:
        return time.time() < payload["isa"] + JWT_EXPIRY_SECONDS

    @staticmethod
    def _get_jwt(
        auth_header: HTTPAuthorizationCredentials = HTTPBearer(auto_error=False),
    ):
        if auth_header is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT not provided"
            )
        return auth_header.credentials

    @staticmethod
    def get_username(
        auth_header: HTTPAuthorizationCredentials = Depends(
            HTTPBearer(auto_error=False)
        ),
    ):
        access_token = AuthenticateService._get_jwt(auth_header)
        payload = AuthenticateService._decode_access_token(access_token)

        if not AuthenticateService.is_valid_token(payload):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired"
            )
        return payload.get("username")
