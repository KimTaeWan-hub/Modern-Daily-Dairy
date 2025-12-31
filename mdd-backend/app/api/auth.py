from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """회원가입"""
    user = AuthService.create_user(db, user_data)
    
    # 회원가입 후 자동 로그인
    login_data = UserLogin(email=user_data.email, password=user_data.password)
    user, access_token = AuthService.authenticate_user(db, login_data)
    
    return Token(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """로그인"""
    user, access_token = AuthService.authenticate_user(db, login_data)
    
    return Token(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_db)):
    """현재 사용자 정보 조회"""
    from app.utils.dependencies import get_current_user
    user = await get_current_user(current_user)
    return UserResponse.model_validate(user)

