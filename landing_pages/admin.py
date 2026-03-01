from django.contrib import admin

# Register your models here.
from .models import LandingPageEntry

class LandingPageEntryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    list_filter =  ['created_at']

admin.site.register(LandingPageEntry, LandingPageEntryAdmin)