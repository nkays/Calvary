#src/sermons/admin.py
from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Sermon, Series

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'series','created_at', 'updated_at')
    list_filter = ('series', 'created_at')
    fields = ['title', 'description', 'youtube_id', 'display_image']
    readonly_fields = ['display_image']

    def display_image(self, obj):
        url = obj.thumbnail  # uses fallback logic
        return format_html('<img src="{}" width="200" />', url)
        
    
    display_image.short_description = "Thumbnail"

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    
    fields = ['title', 'description', 'youtube_playlist_id']