import json

from django.test import TestCase
from django.urls import reverse

from .models import UserProgress


class SimulationPreviewTests(TestCase):
    def test_simulation_index_redirects_to_first_available_preview(self):
        response = self.client.get(reverse('simulations:index'))

        self.assertRedirects(response, reverse('simulations:preview', kwargs={'slug': 'pottery'}))

    def test_pottery_simulation_preview_renders_360_video_activity(self):
        response = self.client.get(reverse('simulations:preview', kwargs={'slug': 'pottery'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'simulations/preview.html')
        self.assertContains(response, 'Arrange the clay preparation, shaping, drying, and firing steps.')
        self.assertContains(response, 'data-panorama-simulation')
        self.assertContains(response, 'data-panorama-canvas')
        self.assertContains(response, 'Play 360 Video')
        self.assertContains(response, 'Verify 360 Visit')
        self.assertContains(response, 'View Passport')
        self.assertContains(response, 'Verified score')
        self.assertContains(response, 'Clay Keeper')
        self.assertContains(response, '/media/simulations/360/pottery.mp4')
        self.assertContains(response, 'Clay wheel')
        self.assertContains(response, reverse('simulations:complete', kwargs={'slug': 'pottery'}))

    def test_complete_simulation_rejects_invalid_360_payload(self):
        response = self.client.post(
            reverse('simulations:complete', kwargs={'slug': 'pottery'}),
            data=json.dumps({'watched_seconds': 'bad', 'coverage_degrees': 360, 'hotspots': []}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], '360 simulation progress contains invalid values.')

    def test_complete_simulation_returns_score_for_partial_360_visit(self):
        response = self.client.post(
            reverse('simulations:complete', kwargs={'slug': 'pottery'}),
            data=json.dumps({
                'watched_seconds': 8,
                'coverage_degrees': 120,
                'hotspots': ['clay-wheel'],
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['completed'])
        self.assertLess(response.json()['score'], 100)

    def test_authenticated_complete_simulation_saves_verified_progress(self):
        from django.contrib.auth.models import User

        user = User.objects.create_user(
            username='learner@example.com',
            email='learner@example.com',
            password='StrongPass12345!',
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse('simulations:complete', kwargs={'slug': 'pottery'}),
            data=json.dumps({
                'watched_seconds': 20,
                'coverage_degrees': 240,
                'hotspots': ['clay-wheel', 'drying-shelf', 'kiln-fire'],
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['completed'])
        progress = UserProgress.objects.get(user=user, hut__slug='pottery')
        self.assertTrue(progress.simulation_completed)
        self.assertEqual(progress.simulation_score, 100)
        self.assertTrue(progress.completed)
        self.assertEqual(progress.score, 100)

    def test_unknown_simulation_returns_404(self):
        response = self.client.get(reverse('simulations:preview', kwargs={'slug': 'unknown'}))

        self.assertEqual(response.status_code, 404)
