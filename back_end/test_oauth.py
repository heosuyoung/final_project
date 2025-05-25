"""
테스트 스크립트: OAuth 디버깅 및 URL 테스트
"""
import requests
import json
import os
import environ
from pathlib import Path

# 환경 변수 로드
BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

def test_oauth_urls():
    """
    백엔드에서 제공하는 OAuth URL을 테스트하여 올바르게 설정되어 있는지 확인합니다.
    """
    base_url = "http://localhost:8000"
    oauth_urls = [
        "/oauth/login/google-oauth2/",
        "/oauth/login/kakao/",
        "/oauth/complete/google-oauth2/",
        "/oauth/complete/kakao/"
    ]
    
    print("OAuth URL 테스트 시작")
    print("-" * 50)
    
    for url in oauth_urls:
        full_url = f"{base_url}{url}"
        print(f"URL 테스트: {full_url}")
        try:
            # HEAD 요청으로 URL 유효성만 확인 (실제 리디렉션 방지)
            response = requests.head(full_url, allow_redirects=False)
            status = response.status_code
            
            if 300 <= status < 400:  # 리디렉션 응답
                print(f"✓ 상태: {status} (리디렉션)")
                location = response.headers.get('Location', '알 수 없음')
                print(f"  리디렉션 URL: {location}")
            else:
                print(f"✓ 상태: {status}")
            
        except requests.RequestException as e:
            print(f"✗ 오류 발생: {str(e)}")
        
        print("-" * 50)

def check_social_auth_settings():
    """
    settings.py의 소셜 로그인 설정을 확인합니다.
    """
    try:
        print("소셜 로그인 설정 확인")
        print("-" * 50)
        
        # SOCIAL_AUTH_KAKAO_KEY 환경변수 확인
        kakao_key = env("SOCIAL_AUTH_KAKAO_KEY", default=None)
        if kakao_key:
            print(f"SOCIAL_AUTH_KAKAO_KEY: {kakao_key[:5]}...{kakao_key[-3:]} (마스킹됨)")
        else:
            print("SOCIAL_AUTH_KAKAO_KEY: 설정되지 않음")
        
        # SOCIAL_AUTH_GOOGLE_OAUTH2_KEY 환경변수 확인
        google_key = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", default=None)
        if google_key:
            print(f"SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: {google_key[:5]}...{google_key[-3:]} (마스킹됨)")
        else:
            print("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: 설정되지 않음")
            
        print("-" * 50)
    except Exception as e:
        print(f"설정 확인 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    print("\n===== OAuth 설정 및 URL 테스트 =====\n")
    check_social_auth_settings()
    test_oauth_urls()
    print("\n테스트 완료")
