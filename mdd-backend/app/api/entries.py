from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.schemas.entry import EntryCreate, EntryUpdate, EntryResponse, EntryListResponse
from app.schemas.integrated import EntryWithTransactionsCreate, EntryWithTransactionsResponse
from app.schemas.transaction import TransactionResponse
from app.services.entry_service import EntryService
from app.services.integrated_service import IntegratedService
from typing import Optional
from datetime import date
from uuid import UUID

router = APIRouter(prefix="/api/entries", tags=["Entries"])


@router.post("", response_model=EntryResponse, status_code=status.HTTP_201_CREATED)
async def create_entry(
    entry_data: EntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """일상 기록 생성"""
    entry = EntryService.create_entry(db, entry_data, current_user)
    return EntryResponse.model_validate(entry)


@router.get("", response_model=EntryListResponse)
async def get_entries(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """일상 기록 목록 조회"""
    skip = (page - 1) * page_size
    entries, total = EntryService.get_entries(
        db, current_user, skip, page_size, start_date, end_date
    )
    
    return EntryListResponse(
        entries=[EntryResponse.model_validate(entry) for entry in entries],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{entry_id}", response_model=EntryResponse)
async def get_entry(
    entry_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """일상 기록 상세 조회"""
    entry = EntryService.get_entry(db, entry_id, current_user)
    return EntryResponse.model_validate(entry)


@router.put("/{entry_id}", response_model=EntryResponse)
async def update_entry(
    entry_id: UUID,
    entry_data: EntryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """일상 기록 수정"""
    entry = EntryService.update_entry(db, entry_id, entry_data, current_user)
    return EntryResponse.model_validate(entry)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(
    entry_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """일상 기록 삭제"""
    EntryService.delete_entry(db, entry_id, current_user)
    return None


# 통합 엔드포인트
@router.post("/with-transactions", response_model=EntryWithTransactionsResponse, status_code=status.HTTP_201_CREATED)
async def create_entry_with_transactions(
    data: EntryWithTransactionsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """일상 기록과 경제 기록 동시 생성"""
    entry, transactions = IntegratedService.create_entry_with_transactions(db, data, current_user)
    
    return EntryWithTransactionsResponse(
        entry=EntryResponse.model_validate(entry),
        transactions=[TransactionResponse.model_validate(t) for t in transactions]
    )


@router.get("/{entry_id}/full", response_model=EntryWithTransactionsResponse)
async def get_entry_with_transactions(
    entry_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """일상 기록과 연관된 경제 기록 함께 조회"""
    entry, transactions = IntegratedService.get_entry_with_transactions(db, entry_id, current_user)
    
    return EntryWithTransactionsResponse(
        entry=EntryResponse.model_validate(entry),
        transactions=[TransactionResponse.model_validate(t) for t in transactions]
    )

