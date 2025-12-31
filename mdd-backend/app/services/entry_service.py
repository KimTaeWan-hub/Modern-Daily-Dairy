from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.entry import Entry
from app.models.user import User
from app.schemas.entry import EntryCreate, EntryUpdate
from typing import Optional
from datetime import date
from uuid import UUID


class EntryService:
    """일상 기록 서비스"""
    
    @staticmethod
    def create_entry(db: Session, entry_data: EntryCreate, user: User) -> Entry:
        """일상 기록 생성"""
        new_entry = Entry(
            user_id=user.id,
            date=entry_data.date,
            title=entry_data.title,
            content=entry_data.content,
            mood=entry_data.mood,
            photos=entry_data.photos,
            tags=entry_data.tags
        )
        
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        
        return new_entry
    
    @staticmethod
    def get_entries(
        db: Session,
        user: User,
        skip: int = 0,
        limit: int = 20,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> tuple[list[Entry], int]:
        """일상 기록 목록 조회"""
        query = db.query(Entry).filter(Entry.user_id == user.id)
        
        # 날짜 필터링
        if start_date:
            query = query.filter(Entry.date >= start_date)
        if end_date:
            query = query.filter(Entry.date <= end_date)
        
        # 총 개수
        total = query.count()
        
        # 페이징 및 정렬 (최신순)
        entries = query.order_by(Entry.date.desc()).offset(skip).limit(limit).all()
        
        return entries, total
    
    @staticmethod
    def get_entry(db: Session, entry_id: UUID, user: User) -> Entry:
        """일상 기록 상세 조회"""
        entry = db.query(Entry).filter(
            Entry.id == entry_id,
            Entry.user_id == user.id
        ).first()
        
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="일상 기록을 찾을 수 없습니다"
            )
        
        return entry
    
    @staticmethod
    def update_entry(
        db: Session,
        entry_id: UUID,
        entry_data: EntryUpdate,
        user: User
    ) -> Entry:
        """일상 기록 수정"""
        entry = EntryService.get_entry(db, entry_id, user)
        
        # 업데이트할 필드만 수정
        update_data = entry_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(entry, field, value)
        
        db.commit()
        db.refresh(entry)
        
        return entry
    
    @staticmethod
    def delete_entry(db: Session, entry_id: UUID, user: User) -> None:
        """일상 기록 삭제"""
        entry = EntryService.get_entry(db, entry_id, user)
        
        db.delete(entry)
        db.commit()

