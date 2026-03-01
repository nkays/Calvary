from django.db import models
from django.utils.text import slugify
from Locations.models import Location  # <-- import here (assuming locations is installed)
from .validators import validate_blocked_email  # <-- import your custom validator

class StaffMember(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    title = models.CharField(max_length=100, blank=True, help_text="e.g. Lead Pastor, Youth Director")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='staff/photos/', blank=True, null=True)
    email = models.EmailField(blank=True, validators=[validate_blocked_email])  # <-- add your custom validator here
    phone = models.CharField(max_length=20, blank=True)
    order = models.PositiveSmallIntegerField(default=0, help_text="For sorting on team pages")
    is_visible = models.BooleanField(default=True, help_text="Show on public team page?")

    # The key tie-in: staff belongs to one primary location (campus/site)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,          # If location deleted, keep staff but null the field
        null=True,
        blank=True,
        related_name='staff_members',       # So from a Location: location.staff_members.all()
        help_text="Primary campus or location this staff member is associated with"
    )

    # Bonus: if you want to link to a user account (for login or contact)
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_profile'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"

    def __str__(self):
        loc_str = f" @ {self.location.title}" if self.location else ""
        return f"{self.name} ({self.title}){loc_str}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def display_title(self):
        return f"{self.title} – {self.location.title}" if self.title and self.location else self.title or self.name