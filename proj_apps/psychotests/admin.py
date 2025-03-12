from django.contrib import admin
from .models import Category, Test, Question, Choice, Result, TestSubmission

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2  # 기본적으로 2개 선택지 제공

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'text', 'order')
    list_filter = ('test',)
    search_fields = ('text',)
    inlines = [ChoiceInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True

class ResultInline(admin.TabularInline):
    model = Result
    extra = 1

class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'views', 'featured', 'created_at')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [QuestionInline, ResultInline]
    date_hierarchy = 'created_at'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}

class ResultAdmin(admin.ModelAdmin):
    list_display = ('test', 'title')
    list_filter = ('test',)
    search_fields = ('title', 'description')

class TestSubmissionAdmin(admin.ModelAdmin):
    list_display = ('test', 'user', 'result', 'created_at')
    list_filter = ('test', 'result')
    date_hierarchy = 'created_at'
    readonly_fields = ('test', 'user', 'result', 'choices', 'created_at')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Result, ResultAdmin)
admin.site.register(TestSubmission, TestSubmissionAdmin)