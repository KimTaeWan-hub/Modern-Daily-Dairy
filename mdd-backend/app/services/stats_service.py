from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.transaction import Transaction, TransactionType
from app.models.user import User
from app.schemas.stats import DailyStats, MonthlyStats, CategoryStats
from datetime import date
from decimal import Decimal
from typing import Optional


class StatsService:
    """통계 서비스"""
    
    @staticmethod
    def get_daily_stats(
        db: Session,
        user: User,
        start_date: date,
        end_date: date
    ) -> list[DailyStats]:
        """일별 통계 조회"""
        
        # 날짜별 수입/지출 집계
        query = db.query(
            Transaction.date,
            Transaction.type,
            func.sum(Transaction.amount).label("total")
        ).filter(
            Transaction.user_id == user.id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).group_by(
            Transaction.date,
            Transaction.type
        ).all()
        
        # 날짜별로 그룹화
        daily_data = {}
        for row in query:
            date_key = row.date
            if date_key not in daily_data:
                daily_data[date_key] = {
                    "income": Decimal("0"),
                    "expense": Decimal("0")
                }
            
            if row.type == TransactionType.INCOME:
                daily_data[date_key]["income"] = row.total
            else:
                daily_data[date_key]["expense"] = row.total
        
        # DailyStats 객체 생성
        stats = []
        for date_key, amounts in daily_data.items():
            stats.append(DailyStats(
                date=date_key,
                total_income=amounts["income"],
                total_expense=amounts["expense"],
                net=amounts["income"] - amounts["expense"]
            ))
        
        return sorted(stats, key=lambda x: x.date)
    
    @staticmethod
    def get_monthly_stats(
        db: Session,
        user: User,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> list[MonthlyStats]:
        """월별 통계 조회"""
        
        query = db.query(
            extract('year', Transaction.date).label('year'),
            extract('month', Transaction.date).label('month'),
            Transaction.type,
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.id).label('count')
        ).filter(
            Transaction.user_id == user.id
        )
        
        # 년/월 필터링
        if year:
            query = query.filter(extract('year', Transaction.date) == year)
        if month:
            query = query.filter(extract('month', Transaction.date) == month)
        
        query = query.group_by(
            extract('year', Transaction.date),
            extract('month', Transaction.date),
            Transaction.type
        ).all()
        
        # 월별로 그룹화
        monthly_data = {}
        for row in query:
            key = (int(row.year), int(row.month))
            if key not in monthly_data:
                monthly_data[key] = {
                    "income": Decimal("0"),
                    "expense": Decimal("0"),
                    "count": 0
                }
            
            if row.type == TransactionType.INCOME:
                monthly_data[key]["income"] = row.total
            else:
                monthly_data[key]["expense"] = row.total
            
            monthly_data[key]["count"] += row.count
        
        # MonthlyStats 객체 생성
        stats = []
        for (year, month), amounts in monthly_data.items():
            stats.append(MonthlyStats(
                year=year,
                month=month,
                total_income=amounts["income"],
                total_expense=amounts["expense"],
                net=amounts["income"] - amounts["expense"],
                transaction_count=amounts["count"]
            ))
        
        return sorted(stats, key=lambda x: (x.year, x.month), reverse=True)
    
    @staticmethod
    def get_category_stats(
        db: Session,
        user: User,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        transaction_type: TransactionType = TransactionType.EXPENSE
    ) -> list[CategoryStats]:
        """카테고리별 통계 조회"""
        
        query = db.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.id).label('count')
        ).filter(
            Transaction.user_id == user.id,
            Transaction.type == transaction_type
        )
        
        # 날짜 필터링
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        query = query.group_by(Transaction.category).all()
        
        # 전체 금액 계산
        total_amount = sum(row.total for row in query)
        
        # CategoryStats 객체 생성
        stats = []
        for row in query:
            percentage = float((row.total / total_amount * 100) if total_amount > 0 else 0)
            stats.append(CategoryStats(
                category=row.category,
                total_amount=row.total,
                transaction_count=row.count,
                percentage=round(percentage, 2)
            ))
        
        return sorted(stats, key=lambda x: x.total_amount, reverse=True)

