from django.contrib import admin

from .models import Bulletin


@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'created_at', 'updated_at')
    ordering = ('-date',)
    search_fields = ('title',)
