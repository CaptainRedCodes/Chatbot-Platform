from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


MIN_PASSWORD_LENGTH = 8
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=MIN_PASSWORD_LENGTH)
    full_name: str = Field(..., min_length=1)


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    full_name: str
    created_at: datetime | None = None


class TokenResponse(BaseModel):
    access_token: str = ""
    refresh_token: str = ""
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    user: UserResponse
    token: TokenResponse


class PasswordResetRequest(BaseModel):
    email: EmailStr

