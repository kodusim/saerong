from django.shortcuts import render
from proj_apps.psychotests.models import Test, Category

def home(request):
    # Get real data from the database instead of hardcoded values
    featured_tests = Test.objects.filter(featured=True).order_by('-created_at')[:5]
    recent_tests = Test.objects.order_by('-created_at')[:6]
    popular_tests = Test.objects.order_by('-views')[:12]
    categories = Category.objects.order_by('order')[:5]
    
    context = {
        'featured_tests': featured_tests,
        'recent_tests': recent_tests,
        'popular_tests': popular_tests,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html', {})

def contact(request):
    # 문의 폼 처리 로직
    if request.method == 'POST':
        # POST 요청 처리 로직 추가
        pass
    
    context = {}
    return render(request, 'core/contact.html', context)
