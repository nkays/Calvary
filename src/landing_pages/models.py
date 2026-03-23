from django.conf import settings
from django.db import models

User =settings.AUTH_USER_MODEL #"auth.User"
# Create your models here.
class LandingPageEntry(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    notes_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name