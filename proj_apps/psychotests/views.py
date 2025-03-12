from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Category, Question, Choice, Result
from django.db.models import F

def test_list(request):
    # Add search functionality 
    query = request.GET.get('q', '')
    
    if query:
        tests = Test.objects.filter(title__icontains=query)
    else:
        tests = Test.objects.all()
    
    categories = Category.objects.all()
    
    context = {
        'tests': tests,
        'categories': categories,
        'query': query,
    }
    return render(request, 'psychotests/test_list.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    tests = Test.objects.filter(category=category)
    
    context = {
        'category': category,
        'tests': tests,
    }
    return render(request, 'psychotests/category_detail.html', context)

def test_detail(request, slug):
    test = get_object_or_404(Test, slug=slug)
    # Increment view count
    Test.objects.filter(id=test.id).update(views=F('views') + 1)
    
    context = {
        'test': test,
    }
    return render(request, 'psychotests/test_detail.html', context)

def take_test(request, slug):
    test = get_object_or_404(Test, slug=slug)
    questions = Question.objects.filter(test=test)
    
    if request.method == 'POST':
        # Process test answers
        # Simple logic - in a real implementation, you'd have more complex scoring
        answers = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                answers[question_id] = value
                
        # Simple logic: just get the first result as a placeholder
        # In a real implementation, you'd calculate the appropriate result based on answers
        result = Result.objects.filter(test=test).first()
        
        if result:
            # Store answers in session for result page
            request.session['test_answers'] = answers
            return redirect('test_result', slug=slug)
        else:
            # Handle case where there are no results defined
            context = {
                'test': test,
                'questions': questions,
                'error': "이 테스트에 결과가 정의되어 있지 않습니다."
            }
            return render(request, 'psychotests/take_test.html', context)
    
    context = {
        'test': test,
        'questions': questions,
    }
    return render(request, 'psychotests/take_test.html', context)

def test_result(request, slug):
    test = get_object_or_404(Test, slug=slug)
    
    # In a real implementation, you'd use the stored answers to determine the correct result
    # For now, we'll just take the first result as a placeholder
    result = Result.objects.filter(test=test).first()
    
    if not result:
        # Create a default message if no results are defined
        result = {
            'title': '결과를 찾을 수 없습니다',
            'description': '이 테스트에 대한 결과가 아직 정의되지 않았습니다.'
        }
    
    context = {
        'test': test,
        'result': result,
    }
    return render(request, 'psychotests/test_result.html', context)

def popular_tests(request):
    # 조회수를 기준으로 인기 테스트 가져오기
    tests = Test.objects.order_by('-views')[:12]
    context = {
        'tests': tests,
        'title': '인기 테스트'
    }
    return render(request, 'psychotests/test_list.html', context)