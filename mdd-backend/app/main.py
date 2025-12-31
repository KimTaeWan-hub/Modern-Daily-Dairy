from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine, Base
from app.api import auth, entries, transactions, stats

settings = get_settings()

# FastAPI 앱 생성
app = FastAPI(
    title="Modern Daily Dairy API",
    description="일상 기록 및 경제 관리 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(entries.router)
app.include_router(transactions.router)
app.include_router(stats.router)


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    # 테이블 생성 (개발 환경에서만 사용, 프로덕션에서는 Alembic 사용)
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")


@app.get("/")
async def root():
    """헬스 체크"""
    return {
        "message": "Modern Daily Dairy API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}

