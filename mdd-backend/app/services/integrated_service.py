from sqlalchemy.orm import Session
from app.models.user import User
from app.models.entry import Entry
from app.models.transaction import Transaction
from app.schemas.integrated import EntryWithTransactionsCreate
from app.services.entry_service import EntryService
from uuid import UUID


class IntegratedService:
    """통합 서비스 (일상 기록 + 경제 기록)"""
    
    @staticmethod
    def create_entry_with_transactions(
        db: Session,
        data: EntryWithTransactionsCreate,
        user: User
    ) -> tuple[Entry, list[Transaction]]:
        """일상 기록과 경제 기록 동시 생성"""
        
        # 1. Entry 생성
        entry = EntryService.create_entry(db, data.entry, user)
        
        # 2. Transactions 생성 (Entry와 연결)
        transactions = []
        for trans_data in data.transactions:
            transaction = Transaction(
                user_id=user.id,
                entry_id=entry.id,  # Entry와 연결
                date=trans_data.date,
                type=trans_data.type,
                category=trans_data.category,
                amount=trans_data.amount,
                description=trans_data.description,
                payment_method=trans_data.payment_method
            )
            db.add(transaction)
            transactions.append(transaction)
        
        db.commit()
        
        # 모든 트랜잭션 refresh
        for transaction in transactions:
            db.refresh(transaction)
        
        return entry, transactions
    
    @staticmethod
    def get_entry_with_transactions(
        db: Session,
        entry_id: UUID,
        user: User
    ) -> tuple[Entry, list[Transaction]]:
        """일상 기록과 연관된 경제 기록 함께 조회"""
        
        # Entry 조회
        entry = EntryService.get_entry(db, entry_id, user)
        
        # Entry와 연관된 Transactions 조회
        transactions = db.query(Transaction).filter(
            Transaction.entry_id == entry_id
        ).all()
        
        return entry, transactions

