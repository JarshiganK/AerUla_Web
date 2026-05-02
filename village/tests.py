from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import SiteViewerSettings


class VillageMapTests(TestCase):
    def test_village_map_renders_hut_navigation(self):
        response = self.client.get(reverse('village:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'village/index.html')
        self.assertContains(response, 'Virtual village')
        self.assertContains(response, 'Pottery Hut')
        self.assertContains(response, 'Palmyrah Craft Hut')
        self.assertContains(response, 'Village Cooking Hut')
        self.assertContains(response, 'Fishing Life Hut')
        self.assertContains(response, 'Folk Music Hut')
        self.assertContains(response, 'Progress 0/5')
        self.assertContains(response, 'data-hut-image=')
        self.assertContains(response, 'Traditional Sri Lankan Pottery')

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
    def test_hut_detail_page_renders_story_activity_and_badge(self):
        response = self.client.get(reverse('village:detail', kwargs={'slug': 'pottery'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'village/detail.html')
        self.assertContains(response, 'Pottery Hut')
        self.assertContains(response, 'Start with context, then try the activity.')
        self.assertContains(response, 'Arrange the clay preparation, shaping, drying, and firing steps.')
        self.assertNotContains(response, 'Why is drying the pot before firing important?')
        self.assertContains(response, 'Clay Keeper')
        self.assertContains(response, 'Browse marketplace')
        self.assertContains(response, 'scene-bench')
        self.assertContains(response, 'River clay')
        self.assertContains(response, 'Tradtional_Sri_Lankan_Pottery.jpg')
        self.assertContains(response, reverse('simulations:preview', kwargs={'slug': 'pottery'}))

    def test_locked_hut_detail_page_renders_preview_state(self):
        response = self.client.get(reverse('village:detail', kwargs={'slug': 'fishing'}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fishing Life Hut')
        self.assertContains(response, 'Story preview')
        self.assertContains(response, 'Preview the story now—it unlocks fully after earlier huts on the path.')

    def test_unknown_hut_returns_404(self):
        response = self.client.get(reverse('village:detail', kwargs={'slug': 'unknown'}))

        self.assertEqual(response.status_code, 404)


class VillageVisibilityGateTests(TestCase):
    def test_village_hidden_for_guests_when_flag_off(self):
        SiteViewerSettings.get_solo()
        SiteViewerSettings.objects.filter(pk=1).update(public_show_virtual_village=False)
        response = self.client.get(reverse('village:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This area is not available right now.')

    def test_village_allowed_for_staff_when_flag_off(self):
        SiteViewerSettings.get_solo()
        SiteViewerSettings.objects.filter(pk=1).update(public_show_virtual_village=False)
        user = User.objects.create_user(
            username='ops@example.com',
            email='ops@example.com',
            password='StrongPass12345!',
            is_staff=True,
        )
        self.client.force_login(user)
        response = self.client.get(reverse('village:index'))
        self.assertContains(response, 'Pottery Hut')
