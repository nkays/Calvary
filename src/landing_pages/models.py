from django.db import models

# Create your models here.
class LandingPageEntry(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name