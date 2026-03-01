from django.db import models

# Create your models here.


class Bulletin(models.Model):
    """A weekly tri-fold bulletin. Stored as six text sections corresponding
    to the panels of a folded brochure.  """

    date = models.DateField(unique=True)
    title = models.CharField(max_length=200, blank=True)
    section1 = models.TextField('Panel 1', blank=True)
    section2 = models.TextField('Panel 2', blank=True)
    section3 = models.TextField('Panel 3', blank=True)
    section4 = models.TextField('Panel 4', blank=True)
    section5 = models.TextField('Panel 5', blank=True)
    section6 = models.TextField('Panel 6', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'bulletin'
        verbose_name_plural = 'bulletins'

    def __str__(self):
        return f"Bulletin for {self.date.isoformat()}"