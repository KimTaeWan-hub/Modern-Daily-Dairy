from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID


class UserCreate(BaseModel):
    """회원가입 스키마"""
    email: EmailStr
    username: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """로그인 스키마"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """사용자 응답 스키마"""
    id: UUID
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """토큰 응답 스키마"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

