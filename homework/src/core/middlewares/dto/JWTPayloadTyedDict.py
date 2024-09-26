from typing import TypedDict


class JwtPayloadTypedDict(TypedDict):
    username: str
    isa: str
    iss: str
