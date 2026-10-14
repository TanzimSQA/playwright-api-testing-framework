from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class LoginSuccessResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    gender: Optional[str] = None
    image: Optional[str] = None
    accessToken: str = Field(..., description="JWT bearer access token")
    refreshToken: Optional[str] = None


class AuthErrorResponse(BaseModel):
    message: str


class CurrentUserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
