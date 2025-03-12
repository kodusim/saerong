from django.contrib import admin
from .models import Banner, Advertisement, Partnership

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'order')

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'position')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)

@admin.register(Partnership)
class PartnershipAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'email', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('company_name', 'contact_person', 'email', 'message')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at',)