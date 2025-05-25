from django.urls import path
from . import views
from . import api  # API 뷰 임포트
from . import token_auth  # 토큰 인증 관련 뷰 임포트
from . import kakao_auth  # 카카오 직접 인증 처리

app_name = 'accounts'

urlpatterns = [
    # 기존 웹 뷰
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:pk>/', views.profile, name='profile'),
    path('<int:pk>/follow/', views.follow, name='follow'),
    
    # REST API 엔드포인트
    path('api/signup/', api.api_signup, name='api_signup'),
    path('api/login/', api.api_login, name='api_login'),
    
    # 토큰 인증 관련 엔드포인트
    path('api/verify-token/', token_auth.verify_token, name='verify_token'),
    path('api/token-status/', token_auth.UserTokenStatusView.as_view(), name='token_status'),
    
    # 카카오 직접 인증 처리
    path('kakao/callback/', kakao_auth.kakao_callback, name='kakao_callback'),
]
