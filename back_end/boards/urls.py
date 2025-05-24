from django.urls import path
from . import views
from .views import get_api_key

app_name="boards"
urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'), 
    path('<int:pk>/update/', views.update, name='update'),   
    path('<int:board_pk>/comment/', views.comment, name='comment'),
    path('<int:board_pk>/comment/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
    path('comment/<int:comment_pk>/', views.create_reply, name='create_reply'),
    path('api/savings/', views.fetch_savings_products, name='fetch_savings_products'),
    path('get-api-key/', get_api_key, name='get_api_key'),
]
