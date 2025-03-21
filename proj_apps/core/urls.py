from django.urls import path
from . import views

app_name = 'core'  # 이 줄을 추가

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]