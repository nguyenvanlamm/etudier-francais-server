from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None


class UserResponse(UserBase):
    id: int
    image: Optional[str] = None
    is_pro: bool
    is_verified: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    user: UserResponse
    accessToken: str
    refreshToken: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class GoogleLoginRequest(BaseModel):
    idToken: str


class RefreshTokenRequest(BaseModel):
    refreshToken: str


class LogoutRequest(BaseModel):
    refreshToken: str