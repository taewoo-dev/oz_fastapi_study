from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi import status


def attach_exception_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return PlainTextResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)
