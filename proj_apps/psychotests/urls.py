from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:slug>/', views.test_detail, name='test_detail'),
    path('<slug:slug>/take/', views.take_test, name='take_test'),
    path('<slug:slug>/result/', views.test_result, name='test_result'),
]