# EA$E 금융 웹 애플리케이션

EA$E는 편리하고 직관적인 금융 웹 애플리케이션입니다. 사용자들에게 금융 정보를 제공하고, 투자 비교 및 자동 투자 기능을 제공합니다.

## 프로젝트 구조

이 프로젝트는 두 부분으로 나뉘어 있습니다:

- `front_end/`: Vue.js 기반의 프론트엔드 애플리케이션
- `back_end/`: Django 기반의 백엔드 API 서버

## 시작하기

### 프론트엔드 설정

```bash
# 필요한 패키지 설치
cd front_end
npm install

# 개발 서버 실행
npm run dev
```

### 백엔드 설정

```bash
# 가상 환경 설정
cd back_end/05_social_projcet
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 필요한 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env  # 그리고 .env 파일에 필요한 값을 입력하세요

# 데이터베이스 마이그레이션
python manage.py migrate

# 서버 실행
python manage.py runserver
```

## 주요 기능

- 사용자 인증 (회원가입, 로그인, 프로필 관리)
- 게시판 기능
- 소셜 로그인 (Google)
- 금융 상품 추천
- 주식 비교 정보
- 자동 투자 기능

## 기술 스택

### 프론트엔드
- Vue 3 (Composition API)
- Vue Router
- Vite
- Axios

### 백엔드
- Django 4.2
- Django REST Framework
- SQLite
- Django Social Auth

## 공동 작업 가이드라인

1. 브랜치 관리
   - `main`: 프로덕션 코드
   - `develop`: 개발 중인 코드
   - 기능 개발은 `feature/기능명` 브랜치에서 작업

2. 코딩 컨벤션
   - JavaScript/Vue: ESLint 규칙 준수
   - Python/Django: PEP 8 규칙 준수

3. 커밋 메시지
   - 기능 추가: `feat: 기능 설명`
   - 버그 수정: `fix: 버그 설명`
   - 문서 수정: `docs: 설명`
   - 리팩토링: `refactor: 설명`
