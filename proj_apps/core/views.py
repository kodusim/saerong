from django.shortcuts import render
from proj_apps.psychotests.models import Test, Category

def home(request):
    # 최신 테스트
    recent_tests = Test.objects.all().order_by('-created_at')[:6]
    
    # 인기 테스트
    popular_tests = Test.objects.all().order_by('-views')[:12]
    
    # 추천 테스트 (Featured)
    featured_tests = Test.objects.filter(featured=True)[:5]
    
    # 카테고리
    categories = Category.objects.all().order_by('order')[:4]
    
    context = {
        'recent_tests': recent_tests,
        'popular_tests': popular_tests,
        'featured_tests': featured_tests,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html', {})

def contact(request):
    return render(request, 'core/contact.html', {})