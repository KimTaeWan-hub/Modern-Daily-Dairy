from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.models.transaction import TransactionType
from app.schemas.stats import DailyStats, MonthlyStats, CategoryStats
from app.services.stats_service import StatsService
from datetime import date, timedelta
from typing import Optional

router = APIRouter(prefix="/api/stats", tags=["Statistics"])


@router.get("/daily", response_model=list[DailyStats])
async def get_daily_stats(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """일별 통계 조회"""
    
    # 기본값: 최근 30일
    if not end_date:
        end_date = date.today()
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    stats = StatsService.get_daily_stats(db, current_user, start_date, end_date)
    return stats


@router.get("/monthly", response_model=list[MonthlyStats])
async def get_monthly_stats(
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """월별 통계 조회"""
    stats = StatsService.get_monthly_stats(db, current_user, year, month)
    return stats


@router.get("/category", response_model=list[CategoryStats])
async def get_category_stats(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    transaction_type: TransactionType = Query(TransactionType.EXPENSE),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """카테고리별 통계 조회"""
    stats = StatsService.get_category_stats(
        db, current_user, start_date, end_date, transaction_type
    )
    return stats

