from sqlalchemy import Column, String, Numeric, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.database import Base


class TransactionType(str, enum.Enum):
    """거래 유형"""
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(Base):
    """경제 기록 모델"""
    
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("entries.id", ondelete="CASCADE"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    type = Column(SQLEnum(TransactionType), nullable=False)
    category = Column(String(100), nullable=False)  # 식비, 교통비, 급여, etc.
    amount = Column(Numeric(12, 2), nullable=False)  # 최대 9,999,999,999.99
    description = Column(String(500), nullable=True)
    payment_method = Column(String(50), nullable=True)  # 현금, 카드, 계좌이체, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    entry = relationship("Entry", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.type}, amount={self.amount}, category={self.category})>"

