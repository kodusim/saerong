from django.contrib import admin
from .models import Category, Test, Question, Choice, Result

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class ResultInline(admin.TabularInline):
    model = Result
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    