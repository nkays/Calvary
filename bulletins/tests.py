from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Bulletin


class BulletinModelTests(TestCase):
    def test_str(self):
        d = timezone.now().date()
        b = Bulletin.objects.create(date=d)
        self.assertEqual(str(b), f"Bulletin for {d.isoformat()}")


class BulletinViewTests(TestCase):
    def setUp(self):
        self.bulletin = Bulletin.objects.create(
            date=timezone.now().date(),
            title='Test',
            section1='A',
            section2='B',
        )

    def test_list_view(self):
        url = reverse('bulletins:list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Test")

    def test_detail_view(self):
        url = reverse('bulletins:detail', args=[self.bulletin.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'A')

    def test_create_view(self):
        url = reverse('bulletins:add')
        future = timezone.now().date() + timezone.timedelta(days=1)
        data = {
            'date': future.isoformat(),
            'title': 'New',
            'section1': '1',
            'section2': '2',
        }
        resp = self.client.post(url, data)
        # successful create should redirect to list
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Bulletin.objects.filter(title='New').exists())

    def test_update_view(self):
        url = reverse('bulletins:update', args=[self.bulletin.pk])
        data = {
            'date': self.bulletin.date.isoformat(),
            'title': 'Updated',
            'section1': 'X',
            'section2': 'Y',
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.bulletin.refresh_from_db()
        self.assertEqual(self.bulletin.title, 'Updated')
