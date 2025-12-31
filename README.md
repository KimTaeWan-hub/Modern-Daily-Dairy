# Modern Daily Dairy

일상 기록과 경제 관리를 통합한 모바일 애플리케이션입니다.

## 프로젝트 구조

```
Modern-Daily-Dairy/
├── mdd-backend/          # FastAPI 백엔드 서버
└── mdd-frontend/         # React Native (Expo) 모바일 앱
```

## 주요 기능

### 🗓️ 일상 기록
- 날짜별 일기 작성
- 감정 상태 기록
- 사진 첨부
- 태그 관리

### 💰 경제 관리
- 수입/지출 기록
- 카테고리별 분류
- 결제 수단 관리
- Entry와 Transaction 통합 관리

### 📊 통계 및 분석
- 일별 지출 추이
- 월별 수입/지출 통계
- 카테고리별 지출 분석
- 시각화된 차트 및 그래프

## 기술 스택

### Backend
- **Framework**: FastAPI 0.110+
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)

### Frontend
- **Framework**: React Native + Expo Router
- **State Management**: Zustand + React Query
- **Charts**: react-native-chart-kit
- **Date Handling**: date-fns
- **HTTP Client**: axios

## 설치 및 실행

### 1. 사전 요구사항

- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Expo CLI

### 2. 백엔드 설정

```bash
cd mdd-backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# PostgreSQL 데이터베이스 생성
psql -U postgres
CREATE DATABASE mdd_db;
CREATE USER mdd_user WITH PASSWORD 'mdd_password';
GRANT ALL PRIVILEGES ON DATABASE mdd_db TO mdd_user;
\q

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 데이터베이스 연결 정보 수정

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

백엔드 API가 http://localhost:8000 에서 실행됩니다.
- API 문서: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. 프론트엔드 설정

```bash
cd mdd-frontend

# 패키지 설치
npm install

# API URL 설정
# lib/api.ts 파일에서 API_BASE_URL을 백엔드 주소로 설정
# 로컬 개발: http://localhost:8000
# 실제 기기 테스트: http://<컴퓨터_IP>:8000

# 앱 실행
npm start

# 플랫폼별 실행
npm run android  # Android
npm run ios      # iOS (Mac만 가능)
npm run web      # 웹 브라우저
```

## API 엔드포인트

### 인증
- `POST /api/auth/signup` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/auth/me` - 현재 사용자 정보

### 일상 기록
- `POST /api/entries` - 일상 기록 생성
- `GET /api/entries` - 목록 조회
- `GET /api/entries/{id}` - 상세 조회
- `PUT /api/entries/{id}` - 수정
- `DELETE /api/entries/{id}` - 삭제

### 경제 기록
- `POST /api/transactions` - 경제 기록 생성
- `GET /api/transactions` - 목록 조회
- `GET /api/transactions/{id}` - 상세 조회
- `PUT /api/transactions/{id}` - 수정
- `DELETE /api/transactions/{id}` - 삭제

### 통합 엔드포인트
- `POST /api/entries/with-transactions` - 일기와 거래 동시 생성
- `GET /api/entries/{id}/full` - 일기와 연관 거래 함께 조회

### 통계
- `GET /api/stats/daily` - 일별 통계
- `GET /api/stats/monthly` - 월별 통계
- `GET /api/stats/category` - 카테고리별 통계

## 데이터베이스 스키마

### Users
- 사용자 계정 정보
- 이메일, 사용자명, 비밀번호 해시

### Entries
- 일상 기록
- 날짜, 제목, 내용, 감정, 사진, 태그

### Transactions
- 경제 거래 기록
- Entry와 연결 가능 (선택사항)
- 날짜, 타입(수입/지출), 카테고리, 금액, 설명

## 화면 구성

### 1. 로그인/회원가입
- 이메일/비밀번호 인증
- JWT 토큰 기반 인증

### 2. 홈 (기록하기)
- 오늘의 일기 작성
- 감정 선택
- 지출/수입 기록
- 통합 저장

### 3. 타임라인
- 과거 기록 목록
- 날짜별 조회
- 카드 형식 표시

### 4. 경제 현황
- 이번 달 수입/지출 요약
- 최근 30일 지출 추이 그래프
- 카테고리별 지출 파이 차트
- 상세 통계

### 5. 프로필
- 사용자 정보
- 로그아웃

## 개발 가이드

### 백엔드 개발

```bash
cd mdd-backend

# 새 API 엔드포인트 추가
# 1. app/schemas/ 에 Pydantic 스키마 정의
# 2. app/services/ 에 비즈니스 로직 구현
# 3. app/api/ 에 라우터 추가
# 4. app/main.py 에 라우터 등록

# 데이터베이스 마이그레이션
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### 프론트엔드 개발

```bash
cd mdd-frontend

# 새 화면 추가
# app/ 폴더에 .tsx 파일 생성 (파일 기반 라우팅)

# API 연동
# lib/api/ 에 API 함수 추가

# 상태 관리
# store/ 에 Zustand 스토어 추가

# 컴포넌트 추가
# components/ 에 재사용 가능한 컴포넌트 생성
```
---

**Created**: 2025-12-31  
**Version**: 1.0.0

