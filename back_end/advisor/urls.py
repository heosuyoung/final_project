from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_with_advisor, name='chat_with_advisor'),
]
