from django.test import TestCase

# Create your tests here.
from .models import LandingPageEntry
from landing_pages import models

class LandingPageEntryTestCase(TestCase):
    def setUp(self):
        LandingPageEntry.objects.create(
            name = "Test Name",
            slug = "test-slug",
            email = "test@example.com",
        )

    def test_landing_page_entry_creation(self):
        entry = LandingPageEntry.objects.get(name="Test Name")
        self.assertEqual(entry.email, "test@example.com")