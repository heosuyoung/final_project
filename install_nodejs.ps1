# Node.js 포터블 버전 다운로드 및 설치 스크립트

Write-Host "Node.js 포터블 버전을 다운로드합니다..." -ForegroundColor Green

# Node.js LTS 버전 URL (Windows x64)
$nodeUrl = "https://nodejs.org/dist/v20.11.1/node-v20.11.1-win-x64.zip"
$downloadPath = "$PSScriptRoot\node-v20.11.1-win-x64.zip"
$extractPath = "$PSScriptRoot\nodejs"

try {
    # 기존 디렉토리가 있으면 삭제
    if (Test-Path $extractPath) {
        Remove-Item $extractPath -Recurse -Force
    }

    # Node.js 다운로드
    Write-Host "다운로드 중..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $nodeUrl -OutFile $downloadPath -UseBasicParsing

    # 압축 해제
    Write-Host "압축 해제 중..." -ForegroundColor Yellow
    Expand-Archive -Path $downloadPath -DestinationPath $PSScriptRoot -Force
    
    # 디렉토리 이름 변경
    $extractedFolder = Get-ChildItem "$PSScriptRoot\node-v*" -Directory | Select-Object -First 1
    Rename-Item $extractedFolder.FullName $extractPath

    # 압축 파일 삭제
    Remove-Item $downloadPath -Force

    # 배치 파일 생성
    $batchContent = @"
@echo off
set PATH=%~dp0nodejs;%PATH%
cd /d "%~dp0front_end"
echo Node.js 버전 확인:
nodejs\node.exe --version
echo NPM 버전 확인:
nodejs\npm.cmd --version
echo.
echo 패키지 설치 중...
nodejs\npm.cmd install
echo.
echo 개발 서버 시작...
nodejs\npm.cmd run dev
pause
"@

    Set-Content -Path "$PSScriptRoot\start_frontend_portable.bat" -Value $batchContent

    Write-Host "✅ Node.js 포터블 설치 완료!" -ForegroundColor Green
    Write-Host "📁 설치 위치: $extractPath" -ForegroundColor Cyan
    Write-Host "🚀 프론트엔드 실행: start_frontend_portable.bat 파일을 실행하세요" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
}
