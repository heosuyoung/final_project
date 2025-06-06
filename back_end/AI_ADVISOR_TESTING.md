# AI 금융 어드바이저 테스트 및 디버깅 가이드

## 필요한 패키지 설치

이 프로젝트는 다음 패키지들을 사용합니다. 설치가 되어있지 않다면 다음 명령어로 설치할 수 있습니다:

```bash
pip install -r requirements.txt
```

## 테스트 스크립트

### 1. CORS 테스트

프론트엔드와 백엔드 간의 통신 문제를 확인하기 위한 CORS 테스트 스크립트:

```bash
python test_cors.py
```

### 2. OpenAI API 테스트

OpenAI API 연결이 정상적으로 작동하는지 확인하는 스크립트:

```bash
python test_openai_api.py
```

## 디버깅 체크리스트

AI 금융 어드바이저 기능이 작동하지 않을 경우 확인할 사항:

1. **브라우저 콘솔 확인**: 
   - 개발자 도구(F12)를 열고 콘솔 탭에서 오류 메시지 확인
   - 네트워크 탭에서 API 요청/응답 확인

2. **CORS 설정 확인**: 
   - `test_cors.py` 실행 후 결과 확인
   - Django settings.py의 CORS 관련 설정 확인

3. **OpenAI API 키 확인**: 
   - `test_openai_api.py` 실행 후 결과 확인
   - API 키가 제대로 설정되어 있는지 확인

4. **백엔드 로그 확인**: 
   - Django 서버의 로그에서 오류 메시지 확인
   - 만약 에러가 발생한다면 해당 에러 로그를 분석

5. **데이터 구조 확인**: 
   - 프론트엔드에서 백엔드로 전송되는 데이터 구조 확인
   - 특히 재무 데이터의 형식이 백엔드에서 예상하는 형식과 일치하는지 확인

## 일반적인 문제 해결

### 1. 백엔드가 응답하지 않음
- Django 서버가 실행 중인지 확인
- 서버 로그에서 에러 확인
- 포트 충돌이 없는지 확인

### 2. OpenAI API 호출 실패
- API 키 유효성 확인
- API 사용량 제한에 도달했는지 확인
- 네트워크 연결 상태 확인

### 3. 메시지 전송 후 대화가 계속되지 않음
- `chatReady` 상태 변수가 제대로 업데이트 되는지 확인
- 네트워크 탭에서 API 호출의 응답 확인
- 타임아웃 설정 확인 (현재 60초로 설정됨)

## 설치된 주요 패키지 목록

- **Django**: 웹 백엔드 프레임워크
- **django-cors-headers**: CORS 지원을 위한 패키지
- **djangorestframework**: REST API 구현을 위한 패키지
- **openai**: OpenAI API 사용을 위한 클라이언트 라이브러리
- **requests**: HTTP 요청 및 API 테스트를 위한 패키지
- **json-log-formatter**: JSON 형식의 로그 생성을 위한 포맷터
- **retry**: 예외 상황에서 함수 재시도를 위한 유틸리티
