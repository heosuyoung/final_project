# EA$E 금융 웹 애플리케이션

EA$E는 사용자 친화적인 금융 정보 제공, 투자 비교, 자동 투자, 커뮤니티 등 다양한 기능을 제공하는 올인원 금융 웹 서비스입니다.

---

## 📁 폴더 구조

```
final_project/
│
├─ front_end/         # Vue3 기반 프론트엔드
│   ├─ public/        # 정적 파일(은행 로고 등)
│   ├─ src/           # Vue 컴포넌트, 라우터, 서비스
│   └─ ...
│
├─ back_end/          # Django 기반 백엔드
│   ├─ accounts/      # 회원/인증/소셜로그인
│   ├─ boards/        # 게시판/댓글
│   ├─ advisor/       # AI 금융상담
│   ├─ api_server/    # 주식/금융 데이터 API
│   └─ ...
│
├─ requirements.txt   # 전체 requirements(통합/개별)
├─ README.md
└─ ...
```

---

## 🚀 실행 방법

### 1. 프론트엔드 (Vue3)

```powershell
cd front_end
npm install
npm run dev
```
- 브라우저에서 http://localhost:5173 접속

### 2. 백엔드 (Django)

```powershell
cd back_end
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
- API 서버: http://localhost:8000

### 3. (선택) 주식 데이터 API 서버
```powershell
cd back_end/api_server
python app.py
```
- Flask 기반 주식 데이터 API (포트: 5000)

---

## 🏦 주요 기능

- **회원가입/로그인/프로필/팔로우**
- **소셜 로그인(Google)**
- **금융상품(예적금) 추천**: 은행별 금리 비교, 조건별 필터, 로고 표시
- **주식 비교/검색/관심종목**
- **자동 투자 시뮬레이션**: 관심종목, 투자 비중, 현황 차트
- **AI 금융상담**: 챗봇 기반 금융 Q&A
- **주식 커뮤니티(게시판)**: 종목별 토론, 글쓰기, 댓글, 인기순/최신순 정렬

---

## ⚙️ 환경설정 및 주의사항

- 프론트엔드: Node.js 18+ 권장, npm 또는 yarn 사용
- 백엔드: Python 3.8+, pip, Django 4.2, requirements.txt 참고
- 은행 로고 등 이미지는 `front_end/public/` 폴더에 png 등으로 직접 추가
- .env 파일(백엔드) 필요시 예시 파일 참고

---

## 💡 기타

- 개발/운영 브랜치 분리 권장 (`main`, `develop`, `feature/`)
- 커밋 메시지: `feat:`, `fix:`, `docs:`, `refactor:` 등 prefix 사용
- 코드 컨벤션: Vue(ESLint), Python(PEP8) 준수

---

**문의/기여/오류 제보는 이슈 또는 PR로 남겨주세요!**
