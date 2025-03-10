from django.shortcuts import render

def home(request):
    # 임시로 간단한 응답 반환
    return render(request, 'core/home.html', {})

def about(request):
    return render(request, 'core/about.html', {})