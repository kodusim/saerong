from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images', blank=True)
    order = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='test_thumbnails')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tests')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    total_questions = models.PositiveIntegerField(default=16, help_text="전체 질문 수")
    selections_count = models.PositiveIntegerField(default=8, help_text="사용자가 선택해야 하는 질문 수")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('psychotests:test_detail', kwargs={'slug': self.slug})

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    image = models.ImageField(upload_to='question_images', blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="비활성화하면 이 질문은 테스트에 표시되지 않습니다")
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.test.title} - Q{self.order}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.TextField()
    image = models.ImageField(upload_to='choice_images', blank=True)
    score_key = models.CharField(max_length=50, help_text="선택 시 특정 결과에 가중치를 부여하는 키(예: A, B, C 등)")
    
    def __str__(self):
        return f"{self.question.test.title} - Q{self.question.order} - {self.text[:20]}"

class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='result_images', blank=True)
    condition = models.TextField(help_text='결과를 결정하는 조건. JSON 형식(예: {"A":">3","B":"<2"})')
    priority = models.IntegerField(default=0, help_text="값이 낮을수록 우선순위가 높습니다(0이 가장 높음)")
    specificity = models.IntegerField(default=0, help_text="이 값이 높을수록 결과 조건이 더 구체적입니다(자동 계산)")
    
    class Meta:
        ordering = ['priority', '-specificity']
    
    def __str__(self):
        return f"{self.test.title} - {self.title}"
        
    def save(self, *args, **kwargs):
        # 조건의 구체성 점수 계산 (조건 개수에 따라)
        try:
            import json
            conditions = json.loads(self.condition)
            self.specificity = len(conditions)
        except:
            self.specificity = 0
        super().save(*args, **kwargs)

class TestSubmission(models.Model):
    """사용자의 테스트 제출 내역을 저장"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='submissions')
    choices = models.JSONField(help_text="사용자가 선택한 답변들을 JSON 형식으로 저장")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        user_info = self.user.username if self.user else "익명"
        return f"{self.test.title} - {user_info} - {self.created_at.strftime('%Y-%m-%d')}"