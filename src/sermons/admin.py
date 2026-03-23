#src/sermons/admin.py
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import format_html


# Register your models here.
from .models import Sermon, Series



class SermonMediaMixin:
    def display_image(self, obj):
        if not obj:
            return ""
        url = obj.thumbnail
        return format_html('<img src="{}" width="200" />', url)

    display_image.short_description = "Thumbnail"

    def display_video(self, obj):
        if not obj or not obj.youtube_id:
            return "No video"

        rendered = render_to_string(
            "pages/snippets/embed.html",
            {
                "embed_url": obj.embed_url,
                "thumbnail_url": obj.thumbnail,
                "title": obj.title,
                "width": 300,
                "height": 170,
            }
        )
        return format_html(rendered)

    display_video.short_description = "Video Preview"

@admin.register(Sermon)
class SermonAdmin(SermonMediaMixin, admin.ModelAdmin):
    list_display = ('title', 'series','created_at', 'updated_at')
    list_filter = ('series', 'created_at')
    fields = ['title', 'description', 'youtube_id', 'published_at']
    readonly_fields = ['display_video', 'display_image']

    
class SermonInline(SermonMediaMixin, admin.TabularInline):
    model = Sermon
    extra = 0
    classes = ['collapse']
    show_change_link = True
    fields = [
        'display_video',   # 👈 move to front (or 2nd)
        'title',
        'youtube_id',
        'description',
        'published_at',
        'status',
        'display_image',
        'access',
            # 👈 move to end
    ]
    readonly_fields = ['display_video', 'display_image'] 
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/video_preview.js',)


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    inlines = [SermonInline]
    list_display = ('title', 'description', 'created_at', 'updated_at')
    
    fields = ['title', 'description', 'youtube_playlist_id','published_at', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

    