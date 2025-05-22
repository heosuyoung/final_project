# 📝 EA$E 금융 웹 애플리케이션 - 백엔드

## 📌 프로젝트 개요
- Django를 활용한 회원 관리 및 게시판 기능 구현
- 로그인, 회원가입, 프로필, 팔로우, 댓글 기능 구현
- Google 소셜 로그인(OAuth 2.0) 구현
- RESTful API 제공으로 프론트엔드 연동

---

## 🔧 설치 및 설정

### 필요 조건
- Python 3.8 이상
- pip 21 이상

### 환경 설정
1. 프로젝트 클론하기
```bash
git clone <repository-url>
cd final_project/back_end/05_social_projcet
```

2. 가상 환경 생성 및 활성화
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env.example` 파일을 `.env`로 복사하고 필요한 설정을 입력하세요:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

5. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

6. 서버 실행
```bash
python manage.py runserver
```

---

## 📁 앱 구성

### 🔐 accounts 앱
- 사용자 모델 커스텀 (AbstractUser 상속)
- 회원가입 / 로그인 / 로그아웃
- 사용자 프로필 (작성 글, 댓글, 팔로워/팔로잉)
- 팔로우 / 언팔로우 기능
- Google 소셜 로그인 구현

### 📝 boards 앱
- 게시글 CRUD (글쓰기, 상세조회, 수정, 삭제)
- 댓글 기능 (작성, 삭제, 대댓글 포함)
- 본인만 수정/삭제 가능

---

## ✅ 기능 요약

| 기능 | 설명 |
|------|------|
| 회원가입 / 로그인 / 로그아웃 | Django 내장 인증 기능 활용 |
| 프로필 페이지 | 본인 글, 댓글, 팔로우 수 등 표시 |
| 팔로우 기능 | 다른 유저 팔로우/언팔로우 가능 |
| 게시판 | 글 작성, 수정, 삭제, 댓글 가능 |
| 댓글 | 대댓글 구조 구현 (`parent_comment`) |
| 소셜 로그인 | Google OAuth2.0 API 적용 |

---

## 🛠 기술 스택

- Python 3.9+
- Django 4.2+
- HTML (Django 템플릿)
- SQLite3
- GCP OAuth 2.0
- `django-environ` (환경변수 관리)

---

## 🔐 .env 예시

```env
SECRET_KEY="your-django-secret-key"
DEBUG=True
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"

##실행방법

# 프로젝트 클론
git clone [레포지토리 주소]
cd [프로젝트 폴더명]

# 가상환경 생성 및 실행
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# .env 파일 생성 (위 예시 참고)

# 마이그레이션 + 관리자 생성
python manage.py migrate
python manage.py createsuperuser

# 서버 실행
python manage.py runserver
