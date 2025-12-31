from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# SQLAlchemy 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # 개발 중 SQL 쿼리 로깅
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스
Base = declarative_base()


def get_db():
    """데이터베이스 세션 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

