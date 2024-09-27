from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi import status

from core.middlewares.exceptions.custom_exceptions import InvalidRefreshTokenException
from users.exceptions.custom_exceptions import (
    UserNotFoundException,
    InvalidPasswordException,
)


def attach_exception_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return PlainTextResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)

    # User API Exception
    @app.exception_handler(UserNotFoundException)
    async def user_not_found_exception_handler(request, exc):
        return JSONResponse(
            content=str(exc),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # JWT Middleware Exception
    @app.exception_handler(InvalidPasswordException)
    async def user_not_found_exception_handler(request, exc):
        return JSONResponse(
            content=str(exc),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    @app.exception_handler(InvalidRefreshTokenException)
    async def user_not_found_exception_handler(request, exc):
        return JSONResponse(
            content=str(exc),
            status_code=status.HTTP_403_FORBIDDEN,
        )
