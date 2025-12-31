from pydantic import BaseModel
from decimal import Decimal
from datetime import date


class DailyStats(BaseModel):
    """일별 통계"""
    date: date
    total_income: Decimal
    total_expense: Decimal
    net: Decimal  # 순수익 (income - expense)


class MonthlyStats(BaseModel):
    """월별 통계"""
    year: int
    month: int
    total_income: Decimal
    total_expense: Decimal
    net: Decimal
    transaction_count: int


class CategoryStats(BaseModel):
    """카테고리별 통계"""
    category: str
    total_amount: Decimal
    transaction_count: int
    percentage: float  # 전체 지출 대비 비율


class StatsResponse(BaseModel):
    """통계 응답"""
    daily_stats: list[DailyStats] = []
    monthly_stats: list[MonthlyStats] = []
    category_stats: list[CategoryStats] = []

