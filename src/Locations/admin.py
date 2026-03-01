from django.contrib import admin

# Register your models here.
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'order',
        'is_visible',
        'url_or_path',
        'created_at',
    )
    
    search_fields = ('title', 'slug', 'url_or_path')
    ordering = ('order', 'title')
    
    fieldsets = (
        ('Main Info', {
            'fields': ('title', 'slug', 'url_or_path')
        }),
        ('Hierarchy & Display', {
            'fields': ('order', 'is_visible', 'css_class', 'icon')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'slug')
    
    
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs