from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.config import get_settings

settings = get_settings()


class AuthService:
    """인증 서비스"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """새 사용자 생성"""
        
        # 이메일 중복 체크
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 등록된 이메일입니다"
            )
        
        # 비밀번호 해싱
        hashed_password = get_password_hash(user_data.password)
        
        # 사용자 생성
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> tuple[User, str]:
        """사용자 인증 및 토큰 발급"""
        
        # 사용자 조회
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다"
            )
        
        # 비밀번호 검증
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다"
            )
        
        # JWT 토큰 생성
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        
        return user, access_token

