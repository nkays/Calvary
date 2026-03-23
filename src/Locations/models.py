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
    
    address = models.ForeignKey(
        'Address', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
        )
    


    photo = models.ImageField(
        upload_to='Locations/photos/', 
        blank=True, 
        null=True)

    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="Auto-generated from title — used in URLs if needed"
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
    
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    # def __str__(self):
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Address(models.Model):
    line_1    = models.CharField("Street address", max_length=100)
    line_2    = models.CharField(max_length=100, blank=True)
    city      = models.CharField(max_length=100)
    state     = models.CharField(max_length=2)   # or CharField(choices=STATE_CHOICES)
    zip_code  = models.CharField(max_length=10)
    country   = models.CharField(max_length=100, default="United States")

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        return f"{self.line_1}, {self.city}, {self.state} {self.zip_code}"

class ServiceTime(models.Model):

    DAYS = [
        ("sun", "Sunday"),
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
    ]

    location = models.ForeignKey(
        Location,
        related_name="services",
        on_delete=models.CASCADE
    )

    day = models.CharField(max_length=3, choices=DAYS, default="sun")

    time = models.TimeField()

    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["day", "order", "time"]

    def __str__(self):
        return f"{self.get_day_display()} {self.time}"