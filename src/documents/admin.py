from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin  # ← The hero import
from .models import Document


@admin.register(Document)
class DocumentAdmin(SummernoteModelAdmin):  # ← Swap ModelAdmin → SummernoteModelAdmin
    list_display = ('title',)
    search_fields = ('title',)

    # Apply Summernote to the 'body' field (your rich text one)
    summernote_fields = ('body',)  # ← This tells it: "Hey, make body fancy!"

    fieldsets = (
        (None, {
            'fields': ('title', 'body',)
        }),
    )