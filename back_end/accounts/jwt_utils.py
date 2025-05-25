"""
JWT 토큰 관리 모듈
"""
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import logging

# 로깅 설정
logger = logging.getLogger(__name__)
User = get_user_model()

def generate_jwt_token(user):
    """
    사용자를 위한 JWT 토큰 생성
    
    Args:
        user: 인증된 사용자 객체
        
    Returns:
        JWT 토큰 문자열
    """
    try:
        # 리프레시 토큰 생성
        refresh = RefreshToken.for_user(user)
        
        # 추가 정보 설정 (payload에 추가)
        refresh['username'] = user.username
        
        # 사용자 이메일이 있는 경우에만 추가
        if hasattr(user, 'email') and user.email:
            refresh['email'] = user.email
        
        # 액세스 토큰 추출
        access_token = str(refresh.access_token)
            
        logger.info(f"JWT 토큰 생성 성공: 사용자 {user.username}")
        return access_token
        
    except Exception as e:
        logger.error(f"JWT 토큰 생성 중 오류 발생: {str(e)}")
        # 예외가 발생해도 기본 토큰은 반환
        return str(RefreshToken.for_user(user).access_token)
