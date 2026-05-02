from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from .services import answer_guide_question


class HomePageTests(TestCase):
    def test_home_page_renders_design_system_content(self):
        response = self.client.get(reverse('core:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Explore Sri Lanka beyond the surface')
        self.assertContains(response, 'Explore the Village')
        self.assertContains(response, 'Browse Experiences')
        self.assertContains(response, 'Ask Guide')
        self.assertContains(response, 'What does the pottery hut teach?')
        self.assertContains(response, 'Authentic cultural references')
        self.assertContains(response, 'Tradtional_Sri_Lankan_Pottery.jpg')


class GuidePageTests(TestCase):
    @override_settings(GEMINI_API_KEY='')
    def test_guide_page_renders_and_references_sources(self):
        response = self.client.get(reverse('core:guide'), {'q': 'pottery'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI Cultural Guide')
        self.assertContains(response, 'pottery')
        self.assertContains(response, 'RAG')

    @override_settings(GEMINI_API_KEY='')
    def test_guide_page_offers_default_prompts(self):
        response = self.client.get(reverse('core:guide'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Continue the conversation')
        self.assertContains(response, 'What does the pottery hut teach?')

    @override_settings(GEMINI_API_KEY='')
    def test_guide_chat_api_returns_grounded_answer(self):
        response = self.client.post(reverse('core:guide_chat_api'), {'message': 'Tell me about pottery'})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('answer', data)
        self.assertIn('sources', data)
        self.assertGreaterEqual(len(data['sources']), 1)
        self.assertContains(response, 'answer', status_code=200)

    @override_settings(GEMINI_API_KEY='')
    def test_guide_page_accepts_chat_message(self):
        response = self.client.post(reverse('core:guide'), {'message': 'Tell me about pottery'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tell me about pottery')
        self.assertContains(response, 'Based on the AerUla village knowledge base')

    @override_settings(GEMINI_API_KEY='test-key', GEMINI_MODEL='gemini-test')
    @patch('core.services._generate_gemini_answer', return_value='Gemini-guided answer')
    def test_guide_question_uses_gemini_when_available(self, mocked_generate):
        response = answer_guide_question('Tell me about pottery', history=[{'user': 'hi', 'assistant': 'hello'}])

        self.assertEqual(response['answer'], 'Gemini-guided answer')
        self.assertEqual(response['mode'], 'gemini')
        self.assertEqual(response['model'], 'gemini-test')
        mocked_generate.assert_called_once()


class RouteTests(TestCase):
    def test_accounts_index_redirects_to_login(self):
        response = self.client.get(reverse('accounts:index'))

        self.assertRedirects(response, reverse('accounts:login'))
