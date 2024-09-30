import time

import jwt
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from core.middlewares.constants.jwt_middleware_constants import (
    JWT_EXPIRY_SECONDS,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)
from core.middlewares.dtos.jwt_payload_typed_dict import JwtPayloadTypedDict
from core.middlewares.exceptions.custom_exceptions import (
    ExpiredTokenException,
    InvalidRefreshTokenException,
)


class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.secret_key = JWT_SECRET_KEY
        self.algorithm = JWT_ALGORITHM

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        auth_header = request.headers.get("Authorization")

        if auth_header is None or not auth_header.startswith("Bearer "):
            return await call_next(request)

        token = auth_header.split(" ")[1]

        try:
            access_token_payload = self._decode_access_token(token)

            if not self._is_valid_token(access_token_payload):
                raise ExpiredTokenException()

            return await call_next(request)

        except ExpiredTokenException:
            refresh_token = request.headers.get("X-Refresh-Token")

            if refresh_token is None:
                raise InvalidRefreshTokenException()

            refresh_token_payload = self._decode_access_token(refresh_token)

            new_access_token = self._create_access_token(
                username=refresh_token_payload["username"]
            )

            response = await call_next(request)

            response.headers["X-Custom-Header"] = new_access_token

            return response

    def _decode_access_token(self, token: JwtPayloadTypedDict) -> dict:
        return jwt.decode(
            jwt=token,
            key=self.secret_key,
            algorithms=[self.algorithm],
        )

    @staticmethod
    def _is_valid_token(payload: JwtPayloadTypedDict) -> bool:
        return time.time() < payload["isa"] + JWT_EXPIRY_SECONDS

    def _create_access_token(self, username: str) -> str:
        payload: JwtPayloadTypedDict = {
            "username": username,
            "isa": time.time(),
            "iss": "oz-coding",
        }
        return jwt.encode(
            payload=payload,
            key=self.secret_key,
            algorithm=JWT_ALGORITHM,
        )
