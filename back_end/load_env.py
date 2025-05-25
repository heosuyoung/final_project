"""
환경 변수 로드 스크립트

이 스크립트는 .env 파일의 환경 변수를 로드하고 출력합니다.
환경 변수가 올바르게 로드되었는지 확인하는 데 사용됩니다.
"""
import os
import environ
from pathlib import Path

# 루트 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent

# 환경 변수 로드
env = environ.Env()
env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

def print_env_vars():
    """
    주요 환경 변수 값을 출력합니다.
    """
    print("\n===== 환경 변수 확인 =====\n")
    
    # Django 설정
    print("Django 설정:")
    print(f"- SECRET_KEY: {'설정됨' if env.get('SECRET_KEY') else '설정되지 않음'}")
    print(f"- DEBUG: {env.bool('DEBUG', default=False)}")
    
    # 소셜 로그인 설정
    print("\n소셜 로그인 설정:")
    
    # Google OAuth2
    google_key = env.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', default=None)
    google_secret = env.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', default=None)
    print(f"- SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: {google_key[:10] + '...' if google_key else '설정되지 않음'}")
    print(f"- SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: {'설정됨' if google_secret else '설정되지 않음'}")
    
    # Kakao OAuth2
    kakao_key = env.get('SOCIAL_AUTH_KAKAO_KEY', default=None)
    kakao_secret = env.get('SOCIAL_AUTH_KAKAO_SECRET', default=None)
    print(f"- SOCIAL_AUTH_KAKAO_KEY: {kakao_key[:10] + '...' if kakao_key else '설정되지 않음'}")
    print(f"- SOCIAL_AUTH_KAKAO_SECRET: {'설정됨' if kakao_secret else '설정되지 않음'}")

if __name__ == "__main__":
    print_env_vars()
