from django.test import TestCase
from django.urls import reverse


class SimulationPreviewTests(TestCase):
    def test_simulation_index_redirects_to_first_available_preview(self):
        response = self.client.get(reverse('simulations:index'))

        self.assertRedirects(response, reverse('simulations:preview', kwargs={'slug': 'pottery'}))

    def test_pottery_simulation_preview_renders_ordering_activity(self):
        response = self.client.get(reverse('simulations:preview', kwargs={'slug': 'pottery'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'simulations/preview.html')
        self.assertContains(response, 'Arrange the clay preparation, shaping, drying, and firing steps.')
        self.assertContains(response, 'data-step-simulation')
        self.assertContains(response, 'Prepare and clean the clay')
        self.assertContains(response, 'Check Order')
        self.assertContains(response, 'Preview score')
        self.assertContains(response, 'Clay Keeper')

    def test_unknown_simulation_returns_404(self):
        response = self.client.get(reverse('simulations:preview', kwargs={'slug': 'unknown'}))

        self.assertEqual(response.status_code, 404)
