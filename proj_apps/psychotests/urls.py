from django.urls import path
from . import views

app_name = 'psychotests'

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('popular/', views.popular_tests, name='popular_tests'),
    path('new/', views.new_tests, name='new_tests'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:slug>/', views.test_detail, name='test_detail'),
    path('<slug:slug>/take/', views.take_test, name='take_test'),
    path('<slug:slug>/result/<int:submission_id>/', views.test_result, name='test_result'),
]