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

    def test_village_map_links_to_hut_detail_pages(self):
        response = self.client.get(reverse('village:index'))

        self.assertContains(response, reverse('village:detail', kwargs={'slug': 'pottery'}))
        self.assertContains(response, reverse('village:detail', kwargs={'slug': 'palmyrah'}))


class HutExperienceTests(TestCase):
    def test_hut_detail_page_renders_story_activity_quiz_and_badge(self):
        response = self.client.get(reverse('village:detail', kwargs={'slug': 'pottery'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'village/detail.html')
        self.assertContains(response, 'Pottery Hut')
        self.assertContains(response, 'Learn the village context first.')
        self.assertContains(response, 'Arrange the clay preparation, shaping, drying, and firing steps.')
        self.assertContains(response, 'Why is drying the pot before firing important?')
        self.assertContains(response, 'Clay Keeper')
        self.assertContains(response, 'Browse Related Products')
        self.assertContains(response, reverse('simulations:preview', kwargs={'slug': 'pottery'}))

    def test_locked_hut_detail_page_renders_preview_state(self):
        response = self.client.get(reverse('village:detail', kwargs={'slug': 'fishing'}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fishing Life Hut')
        self.assertContains(response, 'Story preview')
        self.assertContains(response, 'will unlock after earlier activities')

    def test_unknown_hut_returns_404(self):
        response = self.client.get(reverse('village:detail', kwargs={'slug': 'unknown'}))

        self.assertEqual(response.status_code, 404)
