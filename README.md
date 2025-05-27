# EA$E 금융 웹 애플리케이션

EA$E는 사용자 친화적인 금융 정보 제공, 투자 비교, 자동 투자, 시장 동향 분석, 커뮤니티 등 다양한 기능을 제공하는 올인원 금융 웹 서비스입니다. 실시간 시장 데이터와 AI 금융 상담 기능으로 더 나은 금융 의사결정을 도와드립니다.

---

## 📁 폴더 구조

```
final_project/
│
├─ front_end/         # Vue3 기반 프론트엔드
│   ├─ public/        # 정적 파일(은행 로고, 이미지 등)
│   ├─ src/           
│   │   ├─ components/  # 재사용 가능한 Vue 컴포넌트
│   │   ├─ router/      # Vue Router 설정
│   │   ├─ services/    # API 통신 서비스
│   │   └─ assets/      # 스타일시트, 폰트 등
│   └─ ...
│
├─ back_end/          # Django 기반 백엔드
│   ├─ accounts/      # 회원/인증/소셜로그인 (JWT 포함)
│   ├─ boards/        # 게시판/댓글/좋아요 기능
│   ├─ advisor/       # AI 금융상담 (OpenAI 연동)
│   ├─ api_server/    # 주식/금융 데이터 API (Flask)
│   ├─ crawl/         # 웹 크롤링 스크립트 (네이버 증권 등)
│   └─ ...
│
├─ requirements.txt   # 백엔드 패키지 의존성
├─ package.json       # 프론트엔드 패키지 의존성
├─ start_services.bat # 원클릭 서비스 실행 스크립트
├─ README.md
└─ ...
```

---

## 🚀 실행 방법

### 간편 실행 방법 (권장)

모든 서비스를 한 번에 실행하려면:

```powershell
# 프로젝트 루트 폴더에서
.\start_services.bat
```

이 스크립트는 Django 백엔드, Flask API 서버, Vue.js 프론트엔드를 순차적으로 실행합니다.

### 개별 실행 방법

#### 1. 프론트엔드 (Vue3)

```powershell
# 단일 명령어로 실행
.\start_frontend.bat

# 또는 수동으로 실행
cd front_end
npm install
npm run dev
```
- 브라우저에서 http://localhost:5173 접속

#### 2. 백엔드 (Django)

```powershell
cd back_end
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
- API 서버: http://localhost:8000

#### 3. 주식 데이터 API 서버
```powershell
# 단일 명령어로 실행
.\start_api_server.bat

# 또는 수동으로 실행
cd back_end/api_server
python app.py
```
- Flask 기반 주식 데이터 API (포트: 5000)

---

## 🏦 주요 기능

### 1. 사용자 관리 시스템
- **회원가입/로그인**: 이메일 인증, JWT 토큰 기반 인증
- **소셜 로그인**: Google, Kakao 계정으로 간편 로그인
- **사용자 프로필**: 프로필 사진, 자기소개, 투자 성향 설정
- **팔로우 기능**: 다른 사용자 팔로우하여 활동 및 투자 현황 확인
- **알림 시스템**: 중요 금융 이벤트, 팔로워 활동, 댓글 알림

### 2. 금융상품 비교 및 추천
- **예금/적금 비교**: 은행별, 상품별 최신 금리 비교
- **맞춤형 필터링**: 기간, 금액, 가입 조건별 필터링
- **은행 정보**: 모든 금융기관의 상세 로고 및 정보 표시
- **추천 알고리즘**: 사용자 투자 성향 기반 맞춤 금융상품 추천

### 3. 주식 정보 및 투자
- **종목 검색 및 비교**: 국내외 주요 주식 정보 검색 및 비교
- **관심종목 관리**: 자신만의 관심 종목 리스트 생성 및 관리
- **자동 투자 시뮬레이션**: 설정한 투자 비중에 따른 성과 시뮬레이션
- **실시간 주가 정보**: 네이버 증권 데이터 기반 최신 주가 정보

### 4. 시장 동향 분석
- **주요 시장 지수**: 코스피, 코스닥, 다우존스, 나스닥 등 실시간 지수
- **환율 정보**: USD/KRW, EUR/KRW, JPY/KRW, CNY/KRW 환율 정보
- **상품 가격**: 금, 은, 원유(WTI), 천연가스 등 실시간 가격 정보
- **차트 분석**: 인터랙티브 차트로 추세 분석 및 비교

### 5. AI 금융 상담
- **AI 챗봇**: 금융 관련 질문에 대한 AI 기반 답변 제공
- **투자 조언**: 시장 상황 및 개인 성향에 맞는 투자 조언
- **금융 용어 설명**: 복잡한 금융 용어 쉬운 설명 제공
- **예적금 계산기**: 기간별 예상 수익률 계산

### 6. 커뮤니티
- **종목별 토론방**: 각 주식 종목별 전용 토론방
- **글쓰기/댓글**: 마크다운 지원 글쓰기, 댓글 기능
- **좋아요/북마크**: 유용한 게시물 평가 및 저장
- **정렬 옵션**: 인기순, 최신순, 댓글순 등 다양한 정렬 기능

---

## ⚙️ 환경설정 및 시작하기

### 필수 설치 요소
- **프론트엔드**: Node.js 18+ 및 npm (또는 yarn)
  ```powershell
  # Node.js 설치 스크립트 실행
  .\install_nodejs.ps1
  ```

- **백엔드**: Python 3.8+ 및 pip
  ```powershell
  # 필요한 패키지 설치
  pip install -r requirements.txt
  ```

### 환경 변수 설정
1. 루트 디렉토리에 `.env` 파일 생성 (또는 예제 파일 복사):
   ```
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # 소셜 로그인 설정
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_SECRET=your_google_secret
   
   # OpenAI API (AI 상담용)
   OPENAI_API_KEY=your_openai_api_key
   ```

### 데이터베이스 초기화
```powershell
cd back_end
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 테스트 데이터 로드 (선택사항)
```powershell
# 샘플 금융상품 데이터 로드
python manage.py loaddata sample_financial_products.json

# 주식 시장 데이터 갱신
cd crawl
python crawl_naver_stocks.py
```

---

## 🔧 문제 해결 가이드

### 일반적인 문제
- **프론트엔드 에러**: `npm cache clean --force` 실행 후 재설치
- **백엔드 연결 오류**: CORS 설정 확인 및 Django 서버 재시작
- **API 데이터 누락**: 네트워크 연결 확인 및 네이버 증권 크롤링 재실행

### 디버깅
자세한 디버깅 가이드는 `DEBUGGING_GUIDE.md` 파일을 참조하세요.

---

## 📱 주요 화면 및 기능 사용법

### 메인 페이지
- 주요 시장 동향 정보 확인 (코스피, 환율, 상품 가격)
- 추천 금융상품 및 최근 커뮤니티 게시글 확인

### 금융상품 비교 페이지
- 상단 필터로 원하는 조건 설정 (기간, 금액, 은행 등)
- 각 상품 카드의 "상세보기" 버튼으로 세부정보 확인

### 자동 투자 시뮬레이션
1. "포트폴리오 만들기" 버튼 클릭
2. 관심 종목 선택 및 투자 비중 설정
3. 기간 설정 후 "시뮬레이션 시작" 클릭
4. 차트와 상세 수익률 분석 결과 확인

### AI 상담 기능
- 우측 하단 "AI 상담사" 아이콘 클릭
- 금융 관련 질문 입력 (예: "주식 투자 초보자에게 추천하는 종목은?")
- AI가 맞춤형 답변 제공

---

## 💡 기타

- 모든 기능은 모바일/태블릿에 최적화된 반응형 디자인 적용
- 다크모드 지원: 우측 상단 테마 아이콘으로 전환 가능
- 개발/운영 브랜치 분리 운영 (`main`, `develop`, `feature/`)
- 커밋 메시지: `feat:`, `fix:`, `docs:`, `refactor:` 등 prefix 사용
- 코드 컨벤션: Vue(ESLint), Python(PEP8) 준수

---

**개발 문의/기능 제안/오류 제보는 이슈 또는 PR로 남겨주세요!**
