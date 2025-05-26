@echo off
echo 🚀 주식 분석 서비스 실행 스크립트
echo ====================================

echo.
echo 📦 1단계: 백엔드 패키지 설치 중...
cd /d "c:\Users\HighTech\Desktop\final_project\back_end"
pip install -r requirements.txt

echo.
echo 📦 2단계: 프론트엔드 패키지 설치 중...
cd /d "c:\Users\HighTech\Desktop\final_project\front_end"
npm install

echo.
echo 🌐 3단계: API 서버 시작 중...
cd /d "c:\Users\HighTech\Desktop\final_project\back_end\api_server"
start "API Server" cmd /k "python app.py"

echo.
echo ⏳ API 서버 시작 대기 중... (5초)
timeout /t 5 /nobreak > nul

echo.
echo 🧪 4단계: API 테스트 중...
python test_api.py

echo.
echo 🖥️ 5단계: 프론트엔드 개발 서버 시작 중...
cd /d "c:\Users\HighTech\Desktop\final_project\front_end"
start "Frontend Dev Server" cmd /k "npm run dev"

echo.
echo ✅ 모든 서비스가 시작되었습니다!
echo.
echo 📌 서비스 주소:
echo   - 프론트엔드: http://localhost:5173
echo   - API 서버: http://localhost:5000
echo.
echo 💡 테스트 방법:
echo   1. 브라우저에서 http://localhost:5173 접속
echo   2. 주식 검색에서 '삼성전자' 검색
echo   3. 삼성전자 클릭 후 '분석' 탭 확인
echo   4. 실제 재무정보와 차트가 표시되는지 확인
echo.
echo 🔧 종료 방법: 각 터미널 창에서 Ctrl+C
echo.
pause
