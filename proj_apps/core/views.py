from django.shortcuts import render
from proj_apps.psychotests.models import Test, Category

def home(request):
    # 데이터베이스에서 테스트 가져오기
    try:
        recent_tests = Test.objects.filter(slug__isnull=False).order_by('-created_at')[:6]
        popular_tests = Test.objects.filter(slug__isnull=False).order_by('-views')[:6]
        featured_tests = Test.objects.filter(featured=True, slug__isnull=False).order_by('-created_at')[:5]
        categories = Category.objects.filter(slug__isnull=False).order_by('order')[:5]
    except Exception as e:
        print(f"Error: {e}")
        recent_tests = []
        popular_tests = []
        featured_tests = []
        categories = []
    
    context = {
        'recent_tests': recent_tests,
        'popular_tests': popular_tests,
        'featured_tests': featured_tests,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html', {})