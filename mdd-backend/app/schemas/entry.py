from pydantic import BaseModel, Field
from datetime import date, datetime
from uuid import UUID
from typing import Optional


class EntryBase(BaseModel):
    """일상 기록 기본 스키마"""
    date: date
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[str] = None
    photos: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class EntryCreate(EntryBase):
    """일상 기록 생성 스키마"""
    pass


class EntryUpdate(BaseModel):
    """일상 기록 수정 스키마"""
    date: Optional[date] = None
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[str] = None
    photos: Optional[list[str]] = None
    tags: Optional[list[str]] = None


class EntryResponse(EntryBase):
    """일상 기록 응답 스키마"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class EntryListResponse(BaseModel):
    """일상 기록 목록 응답 스키마"""
    entries: list[EntryResponse]
    total: int
    page: int
    page_size: int

