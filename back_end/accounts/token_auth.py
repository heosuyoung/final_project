"""
토큰 검증 API
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """
    토큰 유효성 검증 API
    
    입력:
    - token: 검증할 토큰 (필수)
    
    출력:
    - 유효한 경우: {"isValid": true, "user": {"id": 1, "username": "username"}}
    - 유효하지 않은 경우: {"isValid": false}
    """
    token_key = request.data.get('token')
    
    # 디버그 로그
    logger.info(f"토큰 검증 요청: {token_key[:5]}..." if token_key else "토큰 없음")
    
    if not token_key:
        return Response({
            "isValid": False,
            "error": "Token is required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # 토큰 존재 여부 확인
        token = Token.objects.filter(key=token_key).first()
        
        if not token:
            logger.warning(f"토큰 검증 실패: 존재하지 않는 토큰")
            return Response({"isValid": False}, status=status.HTTP_200_OK)
        
        # 사용자 정보 가져오기
        user = token.user
        
        # 사용자 상태 확인
        if not user.is_active:
            logger.warning(f"토큰 검증 실패: 비활성화된 사용자 (ID: {user.id})")
            return Response({"isValid": False}, status=status.HTTP_200_OK)
        
        # 유효한 토큰
        logger.info(f"토큰 검증 성공: 사용자 ID {user.id}")
        return Response({
            "isValid": True,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"토큰 검증 중 오류 발생: {str(e)}")
        return Response({
            "isValid": False,
            "error": "Token verification failed"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserTokenStatusView(APIView):
    """
    현재 로그인된 사용자의 토큰 상태 확인
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        token = Token.objects.filter(user=user).first()
        
        return Response({
            "id": user.id,
            "username": user.username,
            "token": token.key if token else None,
            "isAuthenticated": True
        })
