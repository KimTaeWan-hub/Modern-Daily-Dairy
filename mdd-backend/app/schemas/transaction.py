from pydantic import BaseModel, Field
from datetime import date, datetime
from uuid import UUID
from typing import Optional
from decimal import Decimal
from app.models.transaction import TransactionType


class TransactionBase(BaseModel):
    """경제 기록 기본 스키마"""
    date: date
    type: TransactionType
    category: str = Field(..., min_length=1, max_length=100)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    description: Optional[str] = Field(None, max_length=500)
    payment_method: Optional[str] = Field(None, max_length=50)


class TransactionCreate(TransactionBase):
    """경제 기록 생성 스키마"""
    entry_id: Optional[UUID] = None


class TransactionUpdate(BaseModel):
    """경제 기록 수정 스키마"""
    date: Optional[date] = None
    type: Optional[TransactionType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    description: Optional[str] = Field(None, max_length=500)
    payment_method: Optional[str] = Field(None, max_length=50)


class TransactionResponse(TransactionBase):
    """경제 기록 응답 스키마"""
    id: UUID
    entry_id: Optional[UUID] = None
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

