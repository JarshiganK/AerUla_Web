from django.test import TestCase
from django.urls import reverse


class VillageMapTests(TestCase):
    def test_village_map_renders_hut_navigation(self):
        response = self.client.get(reverse('village:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'village/index.html')
        self.assertContains(response, 'Virtual Village Map')
        self.assertContains(response, 'Pottery Hut')
        self.assertContains(response, 'Palmyrah Craft Hut')
        self.assertContains(response, 'Village Cooking Hut')
        self.assertContains(response, 'Fishing Life Hut')
        self.assertContains(response, 'Folk Music Hut')
        self.assertContains(response, 'Progress 0/5')

    def test_village_map_exposes_available_and_locked_states(self):
        response = self.client.get(reverse('village:index'))

        self.assertContains(response, 'data-status="available"', count=3)
        self.assertContains(response, 'data-status="locked"', count=2)
        self.assertContains(response, 'Locked')
        self.assertContains(response, 'Available')
