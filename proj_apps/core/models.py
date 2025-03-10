# apps/core/models.py
from django.db import models

class Banner(models.Model):
    """홈페이지 슬라이더용 배너"""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='banners/')
    url = models.URLField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

class Advertisement(models.Model):
    """광고 배너"""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='advertisements/')
    url = models.URLField()
    position = models.CharField(max_length=50)  # 광고 위치 (메인, 사이드바 등)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class Partnership(models.Model):
    """제휴문의"""
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.company_name} - {self.created_at.strftime('%Y-%m-%d')}"
