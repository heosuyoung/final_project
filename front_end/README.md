# EA$E 금융 웹 애플리케이션 - 프론트엔드

## 프로젝트 소개
EA$E는 사용자 친화적인 금융 웹 애플리케이션으로, 투자 정보 제공, 자동 투자, 주식 비교 등의 기능을 제공합니다.

## 기술 스택
- Vue 3 (Composition API)
- Vue Router
- Vite
- Axios

## 설치 및 실행 방법

### 필요 조건
- Node.js 16 이상
- npm 8 이상

### 설치
```bash
# 패키지 설치
npm install
```

### 개발 서버 실행
```bash
# 개발 서버 실행 (http://localhost:5173/)
npm run dev
```

### 빌드
```bash
# 프로덕션용 빌드
npm run build

# 빌드된 파일 미리보기
npm run preview
```

## 주요 기능
- 사용자 인증 (회원가입, 로그인, 로그아웃)
- 사용자 프로필 관리
- 금융 상품 추천
- 주식 비교 정보
- 자동 투자 기능

## 폴더 구조
- `/src/components`: 재사용 가능한 Vue 컴포넌트
- `/src/services`: API 서비스 관련 파일
- `/public`: 정적 에셋 파일
