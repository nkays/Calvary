from django.db import models

# Create your models here.
from django.utils.text import slugify


class Location(models.Model):
    """
    Flexible model for navigation "locations" — think menu items, nav bar entries,
    footer links, etc. Supports simple hierarchy via parent field.
    """
    title = models.CharField(
        max_length=100,
        help_text="Display name in the navbar (e.g. 'About Us', 'Services')"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="Auto-generated from title — used in URLs if needed"
    )
    
    url_or_path = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="URL or path",
        help_text="Full URL[](https://...) or Django named path (e.g. 'blog:post-list')"
    )
    
    # Alternative: if you prefer strict internal linking
    # view_name = models.CharField(max_length=100, blank=True)  # e.g. 'products:detail'
    # object_id = models.PositiveIntegerField(null=True, blank=True)  # future polymorphic goodness
    
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Lower numbers appear first"
    )
    
    is_visible = models.BooleanField(
        default=True,
        verbose_name="Show in navigation?",
        help_text="Uncheck to hide without deleting"
    )
    
    css_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Extra CSS class (e.g. 'dropdown', 'highlight', 'new-badge')"
    )
    
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome / Heroicon name, e.g. 'fa-solid fa-house'"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Navigation Location"
        verbose_name_plural = "Navigation Locations"

    # def __str__(self):
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # @property
    # def is_top_level(self):
    #     return self.parent is None

    # @property
    # def has_children(self):
    #     return self.children.exists()

