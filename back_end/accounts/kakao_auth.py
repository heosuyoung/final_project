"""
카카오 로그인 직접 처리 모듈
"""
import requests
import json
import os
import random
import string
import environ
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .jwt_utils import generate_jwt_token
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

# .env 파일에서 직접 환경 변수 로드 (설정에 문제가 있을 경우를 대비)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))
User = get_user_model()

def generate_random_string(length=10):
    """무작위 문자열 생성"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def kakao_callback(request):
    """
    카카오 로그인 콜백 - 인증 코드 처리 및 사용자 생성/로그인
    """
    # 인증 코드 확인
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        logger.error(f"카카오 인증 오류: {error}")
        return redirect('http://localhost:5173/oauth/callback?error=kakao_auth_failed&error_description=' + error)
    
    if not code:
        logger.error("카카오 인증 코드 없음")
        return redirect('http://localhost:5173/oauth/callback?error=no_auth_code')
    
    try:
        # 디버그
        logger.info(f"카카오 인증 코드 수신: {code[:10]}...")
          # 카카오 액세스 토큰 요청
        token_url = "https://kauth.kakao.com/oauth/token"
        
        # 먼저 settings에서 API 키를 가져오려고 시도, 실패 시 환경 변수에서 직접 가져옴
        try:
            client_id = settings.SOCIAL_AUTH_KAKAO_KEY
            logger.info(f"설정에서 카카오 API 키 로드: {client_id[:5]}...")
        except AttributeError:
            # settings에 없는 경우 환경 변수에서 직접 로드
            client_id = env('SOCIAL_AUTH_KAKAO_KEY', default='')
            if not client_id:
                client_id = "06a3d74ba43b6ca0c2ab80015a8ad417"  # 하드코딩된 키 (마지막 수단)
            logger.info(f"환경 변수에서 카카오 API 키 로드: {client_id[:5]}...")
            
        redirect_uri = "http://localhost:8000/accounts/kakao/callback/"
        
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'code': code,
        }
        
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        
        # 카카오 API에 토큰 요청
        token_response = requests.post(
            token_url, 
            data=token_data, 
            headers=token_headers
        )
        
        # 요청 실패 처리
        if not token_response.ok:
            logger.error(f"카카오 토큰 요청 실패: {token_response.status_code}")
            logger.error(f"오류 응답: {token_response.text}")
            return redirect('http://localhost:5173/oauth/callback?error=token_request_failed')
        
        # 토큰 응답 파싱
        token_json = token_response.json()
        access_token = token_json.get('access_token')
        
        if not access_token:
            logger.error("카카오 액세스 토큰 없음")
            return redirect('http://localhost:5173/oauth/callback?error=no_access_token')
        
        # 사용자 정보 요청
        user_url = "https://kapi.kakao.com/v2/user/me"
        user_headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        
        user_response = requests.post(user_url, headers=user_headers)
        
        # 요청 실패 처리
        if not user_response.ok:
            logger.error(f"카카오 사용자 정보 요청 실패: {user_response.status_code}")
            return redirect('http://localhost:5173/oauth/callback?error=user_info_failed')
        
        # 사용자 정보 파싱
        user_json = user_response.json()
        kakao_id = user_json.get('id')
        
        if not kakao_id:
            logger.error("카카오 사용자 ID 없음")
            return redirect('http://localhost:5173/oauth/callback?error=no_user_id')
        
        # 기존 사용자 검색 또는 새 사용자 생성
        kakao_user_id = f"kakao_{kakao_id}"
          # 사용자 이름과 이메일 추출 시도
        properties = user_json.get('properties', {})
        kakao_account = user_json.get('kakao_account', {})
        
        # kakao_id를 문자열로 변환하여 처리
        kakao_id_str = str(kakao_id)
        nickname = properties.get('nickname', f"카카오사용자_{kakao_id_str[-6:] if len(kakao_id_str) >= 6 else kakao_id_str}")
        email = kakao_account.get('email', f"{kakao_user_id}@example.com")
        
        # 디버그 출력
        logger.info(f"카카오 사용자 정보: ID={kakao_id}, 닉네임={nickname}")
        
        # 기존 사용자 검색 또는 새로 생성
        try:
            user = User.objects.get(username=kakao_user_id)
            logger.info(f"기존 카카오 사용자 로그인: {user.username}")
        except User.DoesNotExist:
            # 새 사용자 생성
            user = User.objects.create(
                username=kakao_user_id,
                email=email,
            )
            user.set_unusable_password()  # 비밀번호 로그인 불가능하게 설정
            user.save()
            logger.info(f"새 카카오 사용자 생성: {user.username}")
          # 기존 인증 토큰 생성 (하위 호환성 유지)
        token, _ = Token.objects.get_or_create(user=user)
        
        # JWT 토큰 생성 (새로운 인증 방식)
        jwt_token = generate_jwt_token(user)
        
        # 프론트엔드로 리다이렉트 - 토큰 및 사용자 정보 포함
        frontend_url = (
            f"http://localhost:5173/oauth/callback"
            f"?token={token.key}"
            f"&jwt={jwt_token}"
            f"&user_id={user.id}"
            f"&username={nickname}"
            f"&email={email}"
            f"&provider=kakao"
            f"&is_kakao=true"
            f"&success=true"
        )
        
        logger.info(f"카카오 로그인 성공: {user.username}")
        logger.info(f"리다이렉트 URL 생성 완료 (JWT 토큰 포함)")
        
        return redirect(frontend_url)
        
    except Exception as e:
        logger.exception(f"카카오 로그인 처리 중 오류: {str(e)}")
        error_redirect = f"http://localhost:5173/oauth/callback?error=kakao_login_error&message={str(e)}"
        return redirect(error_redirect)
