from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Category, Question, Choice, Result
from django.db.models import F

def test_list(request):
    tests = Test.objects.all()
    categories = Category.objects.all()
    context = {
        'tests': tests,
        'categories': categories,
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
        # Process test answers and redirect to results
        # This is simplified and would need more logic for a real implementation
        return redirect('test_result', slug=slug)
    
    context = {
        'test': test,
        'questions': questions,
    }
    return render(request, 'psychotests/take_test.html', context)

def test_result(request, slug):
    test = get_object_or_404(Test, slug=slug)
    # Placeholder for actual result logic
    result = Result.objects.filter(test=test).first()
    
    context = {
        'test': test,
        'result': result,
    }
    return render(request, 'psychotests/test_result.html', context)