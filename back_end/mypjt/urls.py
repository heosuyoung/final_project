# mypjt/urls.py

from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),  # 추가
    path('boards/', include('boards.urls')),
    path('advisor/', include('advisor.urls')),  # AI 어드바이저 앱 추가
]
