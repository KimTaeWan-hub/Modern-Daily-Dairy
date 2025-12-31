from sqlalchemy import Column, String, Text, Date, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class Entry(Base):
    """일상 기록 모델"""
    
    __tablename__ = "entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    mood = Column(String(50), nullable=True)  # happy, sad, neutral, excited, tired, etc.
    photos = Column(JSON, default=list)  # List of photo URLs
    tags = Column(JSON, default=list)  # List of tags
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="entries")
    transactions = relationship("Transaction", back_populates="entry", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Entry(id={self.id}, date={self.date}, title={self.title})>"

