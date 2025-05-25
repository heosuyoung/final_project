# accounts/social_pipeline.py
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from social_core.pipeline.partial import partial
import logging
import json

User = get_user_model()

# 로깅 설정
logger = logging.getLogger(__name__)

def create_user_token(backend, user, response, *args, **kwargs):
    """
    소셜 로그인 성공 후 사용자 토큰 생성 및 반환
    """
    try:
        # 백엔드 정보 및 응답 디버깅
        logger.info(f"소셜 로그인 성공: {backend.name}")
        logger.info(f"응답 데이터: {json.dumps(response, default=str)}")
        logger.info(f"사용자: {user.username} (ID: {user.id})")
        
        # 소셜 로그인 타입에 따른 처리
        social_type = backend.name
        logger.info(f"소셜 로그인 타입: {social_type}")
        
        # 카카오 로그인인 경우 특별 처리
        is_kakao = social_type == 'kakao'
        if is_kakao:
            logger.info("카카오 로그인 특별 처리 적용")
            print("카카오 로그인 특별 처리 적용")
        
        # 기존 토큰이 있으면 삭제
        Token.objects.filter(user=user).delete()
        
        # 새 토큰 생성
        token = Token.objects.create(user=user)
        
        # 리다이렉트 URL에 token 정보 추가
        # 프론트엔드에서 이 토큰을 사용해 인증
        redirect_url = kwargs.get('redirect_url', '') or kwargs.get('next', '')
        
        if not redirect_url:
            # 기본 리다이렉션 URL 설정 - OAuth 콜백 컴포넌트로
            redirect_url = 'http://localhost:5173/oauth/callback'
        
        # 현재 URL에 이미 쿼리 파라미터가 있는지 확인
        separator = '&' if '?' in redirect_url else '?'
        
        # 리다이렉트 URL 생성 - 토큰, 사용자 ID 및 사용자명 포함
        if is_kakao:
            # 카카오 로그인의 경우 프론트엔드에서 직접 처리하도록 별도의 파라미터 추가
            kwargs['redirect_url'] = f"{redirect_url}{separator}token={token.key}&user_id={user.id}&username={user.username}&provider=kakao&is_kakao=true"
        else:
            # 일반 OAuth 로그인 (구글 등)
            kwargs['redirect_url'] = f"{redirect_url}{separator}token={token.key}&user_id={user.id}&username={user.username}&provider={social_type}"
        
        # 디버깅 출력
        logger.info(f"생성된 토큰: {token.key}")
        logger.info(f"최종 리다이렉트 URL: {kwargs['redirect_url']}")
        print(f"생성된 토큰: {token.key}")
        print(f"소셜 로그인 제공자: {social_type}")
        print(f"리다이렉트 URL: {kwargs['redirect_url']}")
        
        # 응답 형식 통일
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': getattr(user, 'email', ''),
            'provider': social_type
        }
        
        return {'token': token.key, 'user': user, 'user_data': user_data, 'provider': social_type}
        
    except Exception as e:
        # 에러 로깅
        logger.error(f"소셜 로그인 파이프라인 오류: {str(e)}")
        print(f"소셜 로그인 파이프라인 오류: {str(e)}")
        
        # 에러가 발생해도 파이프라인은 계속 진행
        # 기본 리다이렉션 URL로 이동시킴
        kwargs['redirect_url'] = 'http://localhost:5173/oauth/callback?error=token_creation_failed'
        return None
