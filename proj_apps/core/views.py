from django.shortcuts import render

def home(request):
    # 실제 데이터가 없는 초기 상태이므로 간단한 컨텍스트만 전달
    context = {
        'page_title': '홈',
    }
    return render(request, 'core/home.html', context)

def about(request):
    context = {
        'page_title': '소개',
    }
    return render(request, 'core/about.html', context)

def contact(request):
    context = {
        'page_title': '문의하기',
    }
    return render(request, 'core/contact.html', context)