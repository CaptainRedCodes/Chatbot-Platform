from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


MIN_PASSWORD_LENGTH = 8
class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr


class UserCreate(UserBase):
    """User creation schema"""

    password: str = Field(..., min_length=MIN_PASSWORD_LENGTH)
    full_name: str = Field(..., min_length=1)


class UserLogin(UserBase):
    """User login schema"""

    password: str


class UserResponse(UserBase):
    """User response schema"""

    id: str
    full_name: str
    created_at: datetime | None = None


class TokenResponse(BaseModel):
    """Token response schema"""

    access_token: str = ""
    refresh_token: str = ""
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    """Authentication response schema"""

    user: UserResponse
    token: TokenResponse


class PasswordResetRequest(BaseModel):
    """Password reset request schema"""

    email: EmailStr

