#src/sermons/models.py
from re import match

from django.db import models
from google.auth import default

# Create your models here.
'''
    -Sermon Title
        -Title 
        -Description
        -Thumbnail/Image - likely wont need to be stored, can be generated from youtube id     
        -Acess:
            -Anyone (investigate whether logging in is required to save video progress or if youtube can handle this with their own cookies)
    -Status:(may not need this)
        -Published
        -Draft
        -Scheduled
'''
class AccessRequirement(models.TextChoices):
    ANYONE = 'anyone', 'Anyone'
    EMAIL_REQUIRED = 'email', 'Email Required'

class PublishStatus(models.TextChoices):
    PUBLISHED = 'published', 'Published'
    DRAFT = 'draft', 'Draft'
    SCHEDULED = 'scheduled', 'Scheduled'

def handle_upload(instance, filename):
    return f'{filename}'

class Series(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    youtube_playlist_id = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.title

class Sermon(models.Model):
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    published_at = models.DateTimeField(null=True, blank=True)
    access = models.CharField(max_length=20, choices=AccessRequirement.choices, default='anyone')
    status = models.CharField(max_length=20, choices=PublishStatus.choices, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True, related_name='sermons')
   
   
    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


    # Available YouTube thumbnail sizes
    THUMBNAIL_OPTIONS = {
        "small": "default.jpg",
        "medium": "mqdefault.jpg",
        "high": "hqdefault.jpg",
        "standard": "sddefault.jpg",
        "max": "maxresdefault.jpg",
    }


    def get_thumbnail_url(self, size="high"):
        if not self.youtube_id:
            return ""
        filename = self.THUMBNAIL_OPTIONS.get(size, "hqdefault.jpg")
        return f"https://img.youtube.com/vi/{self.youtube_id.strip()}/{filename}"

    @property
    def thumbnail(self):
        return self.get_thumbnail_url("high")
    
    
    
    @property
    def embed_url(self):
        clean_id = self.youtube_id.split("?")[0]
        return f"https://www.youtube-nocookie.com/embed/{clean_id}"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

''' in work below this line, not yet fully implemented, may not even be needed depending on how we want to structure the data.'''
# Lesson.objects.all() -> lesson queryset -> all rows
# Lesson.objects.first() -> lesson object -> first row
# lesson_obj = Sermon.objects.first() -> sermon object -> first row
# Lesson.objects.filter(sermon__id=sermon_obj.id) -> lesson queryset -> all lessons for that sermon
# sermon_obj.lesson_set.all() -> lesson queryset -> all lessons for that sermon
# message_obj = Lesson.objects.first() -> lesson object -> first row
# ne_sermon_obj = lesson_obj.sermon -> sermon object -> sermon for that lesson
# ne_sermon_lessons = ne_sermon_obj.lesson_set.all() -> lesson queryset -> all lessons for that sermon



'''
-Sermon Video
-Title
-Youtube ID (or URL, but ID is likely easier to work with)
-Description  


default.jpg       # small (120x90)
mqdefault.jpg     # medium
hqdefault.jpg     # high quality ✅ (best default)
sddefault.jpg     # standard definition
maxresdefault.jpg # highest quality (not always available ⚠️)      
'''
