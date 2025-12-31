# Modern Daily Dairy - Backend

일상 기록 및 경제 관리 서비스의 백엔드 API 서버입니다.

## 기술 스택

- **Framework**: FastAPI 0.110+
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)

## 설치 및 실행

### 1. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력합니다:

```
DATABASE_URL=postgresql://mdd_user:mdd_password@localhost:5432/mdd_db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. PostgreSQL 데이터베이스 생성

```bash
# PostgreSQL 접속
psql -U postgres

# 데이터베이스 및 사용자 생성
CREATE DATABASE mdd_db;
CREATE USER mdd_user WITH PASSWORD 'mdd_password';
GRANT ALL PRIVILEGES ON DATABASE mdd_db TO mdd_user;
```

### 5. 서버 실행

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면 다음 주소에서 확인할 수 있습니다:
- API: http://localhost:8000
- API 문서 (Swagger): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc

## API 엔드포인트

### 인증 (Authentication)

- `POST /api/auth/signup` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/auth/me` - 현재 사용자 정보

### 일상 기록 (Entries)

- `POST /api/entries` - 일상 기록 생성
- `GET /api/entries` - 일상 기록 목록 조회
- `GET /api/entries/{id}` - 일상 기록 상세 조회
- `PUT /api/entries/{id}` - 일상 기록 수정
- `DELETE /api/entries/{id}` - 일상 기록 삭제

### 경제 기록 (Transactions)

- `POST /api/transactions` - 경제 기록 생성
- `GET /api/transactions` - 경제 기록 목록 조회
- `GET /api/transactions/{id}` - 경제 기록 상세 조회
- `PUT /api/transactions/{id}` - 경제 기록 수정
- `DELETE /api/transactions/{id}` - 경제 기록 삭제

### 통합 엔드포인트

- `POST /api/entries/with-transactions` - 일기와 거래 동시 생성
- `GET /api/entries/{id}/full` - 일기와 연관된 거래 함께 조회

### 통계 (Statistics)

- `GET /api/stats/daily` - 일별 통계
- `GET /api/stats/monthly` - 월별 통계
- `GET /api/stats/category` - 카테고리별 통계

## 프로젝트 구조

```
mdd-backend/
├── app/
│   ├── main.py              # FastAPI 앱 진입점
│   ├── config.py            # 설정 관리
│   ├── database.py          # DB 연결
│   ├── models/              # SQLAlchemy 모델
│   │   ├── user.py
│   │   ├── entry.py
│   │   └── transaction.py
│   ├── schemas/             # Pydantic 스키마
│   │   ├── user.py
│   │   ├── entry.py
│   │   ├── transaction.py
│   │   ├── integrated.py
│   │   └── stats.py
│   ├── api/                 # 라우터
│   │   ├── auth.py
│   │   ├── entries.py
│   │   ├── transactions.py
│   │   └── stats.py
│   ├── services/            # 비즈니스 로직
│   │   ├── auth_service.py
│   │   ├── entry_service.py
│   │   ├── finance_service.py
│   │   ├── integrated_service.py
│   │   └── stats_service.py
│   └── utils/               # 유틸리티
│       ├── auth.py
│       └── dependencies.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 데이터베이스 스키마

### Users
- id (UUID, PK)
- email (unique)
- username
- password_hash
- created_at, updated_at

### Entries
- id (UUID, PK)
- user_id (FK → Users)
- date
- title
- content
- mood
- photos (JSON)
- tags (JSON)
- created_at, updated_at

### Transactions
- id (UUID, PK)
- entry_id (FK → Entries, nullable)
- user_id (FK → Users)
- date
- type (income/expense)
- category
- amount
- description
- payment_method
- created_at, updated_at

## 개발

### 테스트 실행

```bash
pytest
```

### 코드 포맷팅

```bash
black app/
```

### 타입 체크

```bash
mypy app/
```

