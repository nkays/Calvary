from django.contrib import admin

# Register your models here.
from .models import Location, Address, ServiceTime

class ServiceTimeInline(admin.TabularInline):
    model = ServiceTime
    extra = 1  # Number of extra forms to display
    max_num = 7  # Limit to 7 service times (one per day)




@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = [ServiceTimeInline]
    list_display = (
        'title',
        'order',
        'is_visible',
        'created_at',
    )
    
    search_fields = ('title', 'slug',)
    ordering = ('order', 'title')
    
    fieldsets = (
        ('Main Info', {
            'fields': ('title', 'slug', 'address','photo')
        }),
        ('Hierarchy & Display', {
            'fields': ('order', 'is_visible')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'slug')
    
    
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs
    
@admin.register(Address)
class AdressAdmin(admin.ModelAdmin):
    list_display = (
        'city',
    )


class ServiceTimeInline(admin.TabularInline):
    model = ServiceTime
    extra = 1  # Number of extra forms to display
    max_num = 7  # Limit to 7 service times (one per day)

