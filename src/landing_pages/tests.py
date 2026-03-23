from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.
from .models import LandingPageEntry
from landing_pages import models


User = get_user_model()

class LandingPageEntryTestCase(TestCase):
    fixtures = ['entry-data.json', 'users.json']
    def setUp(self):
        LandingPageEntry.objects.create(
            name = "Test Name",
            slug = "test-slug",
            email = "test@example.com",
        )

    def test_landing_page_entry_creation(self):
        entry = LandingPageEntry.objects.get(name="Test Name")
        self.assertEqual(entry.email, "test@example.com")

    def test_users_exist(self):
        qs = User.objects.all()
        self.assertTrue(qs.exists())