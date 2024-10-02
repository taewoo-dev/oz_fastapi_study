from pydantic import BaseModel, constr, Field


class UserCreateRequestDto(BaseModel):
    username: str
    password: str


class UserSignInRequestDto(BaseModel):
    username: str
    password: str


class UserUpdateRequestDto(BaseModel):
    password: str | None


EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


class UserOtpRequestDto(BaseModel):
    email: constr(pattern=EMAIL_PATTERN) = Field(examples=["examples@email.com"])


class UserOtpVerifyRequestDto(BaseModel):
    email: constr(pattern=EMAIL_PATTERN) = Field(examples=["examples@email.com"])
    otp: Field(..., ge=100_000, le=999_999)
