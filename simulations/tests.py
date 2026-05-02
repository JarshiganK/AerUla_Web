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
        self.assertContains(response, reverse('simulations:quiz', kwargs={'slug': 'pottery'}))
        self.assertContains(response, 'Preview score')
        self.assertContains(response, 'Clay Keeper')

    def test_quiz_renders_checkpoint_question(self):
        response = self.client.get(reverse('simulations:quiz', kwargs={'slug': 'pottery'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'simulations/quiz.html')
        self.assertContains(response, 'Why is drying the pot before firing important?')
        self.assertContains(response, 'Check Answer')
        self.assertContains(response, 'Clay Keeper')

    def test_quiz_post_shows_badge_preview_for_correct_answer(self):
        response = self.client.post(
            reverse('simulations:quiz', kwargs={'slug': 'pottery'}),
            {'answer': 'It helps the clay harden evenly'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Badge preview unlocked.')

    def test_unknown_simulation_returns_404(self):
        response = self.client.get(reverse('simulations:preview', kwargs={'slug': 'unknown'}))

        self.assertEqual(response.status_code, 404)

    def test_unknown_quiz_returns_404(self):
        response = self.client.get(reverse('simulations:quiz', kwargs={'slug': 'unknown'}))

        self.assertEqual(response.status_code, 404)
