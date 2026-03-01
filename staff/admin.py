from django.contrib import admin
from .models import StaffMember


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'location', 'is_visible', 'order')
    list_filter = ('is_visible', 'location')
    search_fields = ('name', 'title', 'bio')
    prepopulated_fields = {'slug': ('name',)}  # auto-slug from name
    fieldsets = (
        ('Basics', {'fields': ('name', 'slug', 'title', 'location', 'order', 'is_visible')}),
        ('Contact & Media', {'fields': ('email', 'phone', 'photo', 'bio')}),
        ('User Link', {'fields': ('user',), 'classes': ('collapse',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at', 'updated_at')