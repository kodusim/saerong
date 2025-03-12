from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import F, Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
import random

from .models import Test, Category, Question, Choice, Result, TestSubmission

def test_list(request):
    tests = Test.objects.all()
    categories = Category.objects.all()
    
    # 검색 기능
    query = request.GET.get('q')
    if query:
        tests = tests.filter(title__icontains=query)
    
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
    
    # 테스트 정보 가져오기
    total_questions = test.total_questions
    selections_count = test.selections_count
    
    context = {
        'test': test,
        'total_questions': total_questions,
        'selections_count': selections_count,
    }
    return render(request, 'psychotests/test_detail.html', context)

def take_test(request, slug):
    test = get_object_or_404(Test, slug=slug)
    
    # 테스트에 필요한 정보 가져오기
    total_questions = test.total_questions
    selections_count = test.selections_count
    
    # 모든 활성화된 질문 가져오기
    all_questions = Question.objects.filter(test=test, is_active=True).order_by('order')
    
    # 질문이 total_questions보다 적으면 예외 처리
    if all_questions.count() < total_questions:
        messages.error(request, "테스트 설정에 문제가 있습니다. 관리자에게 문의하세요.")
        return redirect('psychotests:test_detail', slug=slug)
    
    # 사용자가 질문 수보다 더 많은 선택을 해야 하는 경우 예외 처리
    if selections_count > all_questions.count():
        messages.error(request, "테스트 설정에 문제가 있습니다. 관리자에게 문의하세요.")
        return redirect('psychotests:test_detail', slug=slug)
    
    # 테스트에 사용할 질문 선택
    # 전체 질문이 total_questions개 이하면 모든 질문 사용, 아니면 랜덤 선택
    if all_questions.count() <= total_questions:
        test_questions = all_questions
    else:
        # 랜덤하게 total_questions 개수만큼 선택
        question_ids = list(all_questions.values_list('id', flat=True))
        selected_ids = random.sample(question_ids, total_questions)
        test_questions = Question.objects.filter(id__in=selected_ids).order_by('order')
    
    if request.method == 'POST':
        # 사용자 선택 수집
        choices_data = {}
        score_counts = {}
        
        for question_id in request.POST.getlist('question_ids'):
            choice_id = request.POST.get(f'question_{question_id}')
            if choice_id:
                try:
                    choice = Choice.objects.get(id=choice_id)
                    choices_data[question_id] = {
                        'choice_id': choice_id,
                        'score_key': choice.score_key
                    }
                    
                    # 점수 집계
                    score_key = choice.score_key
                    if score_key in score_counts:
                        score_counts[score_key] += 1
                    else:
                        score_counts[score_key] = 1
                except Choice.DoesNotExist:
                    continue
        
        # 선택한 질문 수 확인
        if len(choices_data) < selections_count:
            messages.error(request, f"모든 질문({selections_count}개)에 답변해주세요.")
            context = {
                'test': test,
                'questions': test_questions,
                'selections_count': selections_count,
            }
            return render(request, 'psychotests/take_test.html', context)
        
        # 결과 결정 (개선된 로직)
        chosen_result = determine_test_result(test, score_counts)
        
        if chosen_result:
            # 결과 저장
            submission = TestSubmission(
                test=test,
                result=chosen_result,
                choices=choices_data
            )
            
            # 로그인한 사용자라면 연결
            if request.user.is_authenticated:
                submission.user = request.user
            
            submission.save()
            
            # 결과 페이지로 리다이렉트
            return redirect('psychotests:test_result', slug=slug, submission_id=submission.id)
        else:
            messages.error(request, "결과를 결정할 수 없습니다. 관리자에게 문의하세요.")
            return redirect('psychotests:test_detail', slug=slug)
    
    context = {
        'test': test,
        'questions': test_questions,
        'selections_count': selections_count,
    }
    return render(request, 'psychotests/take_test.html', context)

def determine_test_result(test, score_counts):
    """
    사용자의 선택에 따라 적절한 결과를 결정하는 함수
    
    Args:
        test: 테스트 객체
        score_counts: 사용자의 선택에 따른 점수 집계 (예: {'A': 3, 'B': 5})
        
    Returns:
        Result 객체 또는 None (적절한 결과가 없을 경우)
    """
    # 결과를 우선순위 순으로 정렬 (priority 오름차순, specificity 내림차순)
    results = Result.objects.filter(test=test).order_by('priority', '-specificity')
    
    matching_results = []
    
    for result in results:
        try:
            # JSON 조건 파싱
            conditions = json.loads(result.condition)
            match_score = 0
            total_conditions = len(conditions)
            all_matched = True
            
            # 각 조건 확인
            for key, condition_expr in conditions.items():
                operator = condition_expr[0]  # '>', '<', '=', etc.
                value = int(condition_expr[1:])
                actual_value = score_counts.get(key, 0)
                
                condition_matched = False
                
                if operator == '>' and actual_value > value:
                    condition_matched = True
                elif operator == '<' and actual_value < value:
                    condition_matched = True
                elif operator == '=' and actual_value == value:
                    condition_matched = True
                elif operator == '>=' and actual_value >= value:
                    condition_matched = True
                elif operator == '<=' and actual_value <= value:
                    condition_matched = True
                
                if condition_matched:
                    match_score += 1
                else:
                    all_matched = False
            
            # 매칭 정도 계산 (0.0 ~ 1.0)
            match_percentage = match_score / total_conditions if total_conditions > 0 else 0
            
            # 모든 조건이 일치하거나, 일치율이 0.7 이상인 경우 (70% 이상 일치)
            if all_matched or match_percentage >= 0.7:
                matching_results.append({
                    'result': result,
                    'match_percentage': match_percentage,
                    'all_matched': all_matched,
                    'priority': result.priority,
                    'specificity': result.specificity
                })
        except json.JSONDecodeError:
            # JSON 파싱 실패시 단순 비교 (A>3 형식)
            try:
                condition = result.condition.strip()
                if '>' in condition:
                    parts = condition.split('>')
                    key, value = parts[0].strip(), int(parts[1].strip())
                    if score_counts.get(key, 0) > value:
                        matching_results.append({
                            'result': result,
                            'match_percentage': 1.0,
                            'all_matched': True,
                            'priority': result.priority,
                            'specificity': 1
                        })
                elif '<' in condition:
                    parts = condition.split('<')
                    key, value = parts[0].strip(), int(parts[1].strip())
                    if score_counts.get(key, 0) < value:
                        matching_results.append({
                            'result': result,
                            'match_percentage': 1.0,
                            'all_matched': True,
                            'priority': result.priority,
                            'specificity': 1
                        })
                elif '=' in condition:
                    parts = condition.split('=')
                    key, value = parts[0].strip(), int(parts[1].strip())
                    if score_counts.get(key, 0) == value:
                        matching_results.append({
                            'result': result,
                            'match_percentage': 1.0,
                            'all_matched': True,
                            'priority': result.priority,
                            'specificity': 1
                        })
            except (ValueError, IndexError):
                continue
    
    # 결과가 없으면 None 반환
    if not matching_results:
        # 일치하는 결과가 없을 경우 첫 번째 결과 반환 (폴백)
        if results.exists():
            return results.first()
        return None
    
    # 결과 선택 로직:
    # 1. 모든 조건이 일치하는 결과 중에서
    exact_matches = [r for r in matching_results if r['all_matched']]
    if exact_matches:
        # 2. 우선순위가 가장 높은 결과 중에서 (priority 값이 작을수록 우선순위 높음)
        min_priority = min(r['priority'] for r in exact_matches)
        highest_priority_matches = [r for r in exact_matches if r['priority'] == min_priority]
        
        # 3. 가장 구체적인 조건을 가진 결과 선택 (specificity 값이 클수록 구체적)
        if highest_priority_matches:
            return max(highest_priority_matches, key=lambda x: x['specificity'])['result']
    
    # 정확히 일치하는 결과가 없으면, 부분 일치하는 결과 중 가장 일치율이 높은 결과 선택
    return max(matching_results, key=lambda x: (x['match_percentage'], x['specificity']))['result']

def test_result(request, slug, submission_id):
    test = get_object_or_404(Test, slug=slug)
    
    # 제출 기록 확인 (타인의 제출 결과를 볼 수 없도록 제한)
    if request.user.is_authenticated:
        # 키워드 인수로 통일
        submission = get_object_or_404(
            TestSubmission,
            id=submission_id,
            test=test,
            user__in=[request.user, None]  # user가 현재 사용자이거나 None인 경우
        )
    else:
        # 비로그인 사용자는 익명 제출 결과만 볼 수 있음
        submission = get_object_or_404(
            TestSubmission,
            id=submission_id,
            test=test,
            user__isnull=True
        )
    
    result = submission.result
    
    # 다른 결과 확인 (최대 3개)
    other_results = Result.objects.filter(test=test).exclude(id=result.id).order_by('?')[:3]
    
    # 공유 링크 생성
    share_url = request.build_absolute_uri()
    
    context = {
        'test': test,
        'result': result,
        'submission': submission,
        'other_results': other_results,
        'share_url': share_url,
    }
    return render(request, 'psychotests/test_result.html', context)

# 추가 뷰: 인기 테스트
def popular_tests(request):
    # 조회수 기준 인기 테스트
    tests = Test.objects.order_by('-views')[:12]
    context = {
        'tests': tests,
        'title': '인기 테스트'
    }
    return render(request, 'psychotests/test_list.html', context)

# 추가 뷰: 새 테스트
def new_tests(request):
    # 최신 테스트
    tests = Test.objects.order_by('-created_at')[:12]
    context = {
        'tests': tests,
        'title': '최신 테스트'
    }
    return render(request, 'psychotests/test_list.html', context)