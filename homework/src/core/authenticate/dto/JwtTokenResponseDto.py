from typing import TypedDict

from pydantic import BaseModel


class JwtPayloadTypedDict(TypedDict):
    username: str
    isa: str
    iss: str


class JwtTokenResponseDto(BaseModel):
    access_token: str
    refresh_token: str

    @classmethod
    def build(cls, access_token: str, refresh_token: str):
        return cls(access_token=access_token, refresh_token=refresh_token)
