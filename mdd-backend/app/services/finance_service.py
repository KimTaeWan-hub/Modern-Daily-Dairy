from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from typing import Optional
from datetime import date
from uuid import UUID


class FinanceService:
    """경제 관리 서비스"""
    
    @staticmethod
    def create_transaction(
        db: Session,
        transaction_data: TransactionCreate,
        user: User
    ) -> Transaction:
        """경제 기록 생성"""
        new_transaction = Transaction(
            user_id=user.id,
            entry_id=transaction_data.entry_id,
            date=transaction_data.date,
            type=transaction_data.type,
            category=transaction_data.category,
            amount=transaction_data.amount,
            description=transaction_data.description,
            payment_method=transaction_data.payment_method
        )
        
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        
        return new_transaction
    
    @staticmethod
    def get_transactions(
        db: Session,
        user: User,
        skip: int = 0,
        limit: int = 50,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category: Optional[str] = None,
        transaction_type: Optional[str] = None
    ) -> tuple[list[Transaction], int]:
        """경제 기록 목록 조회"""
        query = db.query(Transaction).filter(Transaction.user_id == user.id)
        
        # 날짜 필터링
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        # 카테고리 필터링
        if category:
            query = query.filter(Transaction.category == category)
        
        # 타입 필터링
        if transaction_type:
            query = query.filter(Transaction.type == transaction_type)
        
        # 총 개수
        total = query.count()
        
        # 페이징 및 정렬 (최신순)
        transactions = query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()
        
        return transactions, total
    
    @staticmethod
    def get_transaction(db: Session, transaction_id: UUID, user: User) -> Transaction:
        """경제 기록 상세 조회"""
        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user.id
        ).first()
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="경제 기록을 찾을 수 없습니다"
            )
        
        return transaction
    
    @staticmethod
    def update_transaction(
        db: Session,
        transaction_id: UUID,
        transaction_data: TransactionUpdate,
        user: User
    ) -> Transaction:
        """경제 기록 수정"""
        transaction = FinanceService.get_transaction(db, transaction_id, user)
        
        # 업데이트할 필드만 수정
        update_data = transaction_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(transaction, field, value)
        
        db.commit()
        db.refresh(transaction)
        
        return transaction
    
    @staticmethod
    def delete_transaction(db: Session, transaction_id: UUID, user: User) -> None:
        """경제 기록 삭제"""
        transaction = FinanceService.get_transaction(db, transaction_id, user)
        
        db.delete(transaction)
        db.commit()

