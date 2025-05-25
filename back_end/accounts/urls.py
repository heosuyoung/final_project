from django.urls import path
from . import views
from . import api  # API 뷰 임포트

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
]
