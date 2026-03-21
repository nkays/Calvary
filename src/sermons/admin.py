#src/sermons/admin.py
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import format_html
from mistune import html

# Register your models here.
from .models import Sermon, Series

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'series','created_at', 'updated_at')
    list_filter = ('series', 'created_at')
    fields = ['title', 'description', 'youtube_id', 'published_at','display_video', 'display_image']
    readonly_fields = ['display_video', 'display_image']

    def display_image(self, obj):
        url = obj.thumbnail  # uses fallback logic
        return format_html('<img src="{}" width="200" />', url)
        
    
    display_image.short_description = "Thumbnail"
    
    def display_video(self, obj):
        if not obj.youtube_id:
            return "No video"

        html = render_to_string(
            "pages/snippets/embed.html",
            {
                "embed_url": obj.embed_url,
                "width": 300,
                "height": 170,
            }
        )

        return format_html(html)

    display_video.short_description = "Video Preview"

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    
    fields = ['title', 'description', 'youtube_playlist_id']