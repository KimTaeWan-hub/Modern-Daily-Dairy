from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services.finance_service import FinanceService
from typing import Optional
from datetime import date
from uuid import UUID

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """경제 기록 생성"""
    transaction = FinanceService.create_transaction(db, transaction_data, current_user)
    return TransactionResponse.model_validate(transaction)


@router.get("", response_model=list[TransactionResponse])
async def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    transaction_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """경제 기록 목록 조회"""
    transactions, total = FinanceService.get_transactions(
        db, current_user, skip, limit, start_date, end_date, category, transaction_type
    )
    
    return [TransactionResponse.model_validate(t) for t in transactions]


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """경제 기록 상세 조회"""
    transaction = FinanceService.get_transaction(db, transaction_id, current_user)
    return TransactionResponse.model_validate(transaction)


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: UUID,
    transaction_data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """경제 기록 수정"""
    transaction = FinanceService.update_transaction(db, transaction_id, transaction_data, current_user)
    return TransactionResponse.model_validate(transaction)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """경제 기록 삭제"""
    FinanceService.delete_transaction(db, transaction_id, current_user)
    return None

