from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from marketplace.cart import CART_SESSION_KEY
from marketplace.models import Product

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
    def test_guide_chat_api_does_not_force_default_hut_for_unmatched_question(self):
        response = self.client.post(reverse('core:guide_chat_api'), {'message': 'Jarshigan'})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['sources'], [])
        self.assertIn('could not find an AerUla knowledge-base match', data['answer'])
        self.assertNotIn('Pottery Hut is the closest match', data['answer'])

    @override_settings(GEMINI_API_KEY='')
    def test_guide_chat_api_prioritizes_bookable_experience_for_booking_intent(self):
        response = self.client.post(reverse('core:guide_chat_api'), {'message': 'book pottery'})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['sources'][0]['title'], 'Pottery Workshop Visit')
        self.assertEqual(data['sources'][0]['source_label'], 'Bookable experience')
        self.assertIn(reverse('bookings:request', kwargs={'slug': 'pottery-workshop'}), data['sources'][0]['url'])
        self.assertIn('cannot submit the booking for you in chat yet', data['answer'])
        self.assertNotIn('Clay Serving Bowl is the closest match', data['answer'])

    @override_settings(GEMINI_API_KEY='')
    def test_guide_chat_api_uses_previous_hut_for_booking_follow_up(self):
        first_response = self.client.post(reverse('core:guide_chat_api'), {'message': 'book pottery'})
        self.assertEqual(first_response.status_code, 200)

        follow_up = self.client.post(reverse('core:guide_chat_api'), {'message': 'can you book for me'})

        self.assertEqual(follow_up.status_code, 200)
        data = follow_up.json()
        self.assertEqual(data['sources'][0]['title'], 'Pottery Workshop Visit')
        self.assertEqual(data['sources'][0]['source_label'], 'Bookable experience')
        self.assertNotIn('Folk Song Booklet', data['answer'])

    @override_settings(GEMINI_API_KEY='')
    def test_guide_chat_api_adds_clear_product_to_cart(self):
        product = Product.objects.get(slug='clay-serving-bowl')
        response = self.client.post(reverse('core:guide_chat_api'), {'message': 'add Clay Serving Bowl to cart'})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('I added Clay Serving Bowl to your cart', data['answer'])
        self.assertEqual(data['sources'][0]['title'], 'Clay Serving Bowl')
        self.assertEqual(data['actions'][0]['url'], reverse('marketplace:checkout'))
        self.assertEqual(self.client.session[CART_SESSION_KEY], {str(product.pk): 1})

    @override_settings(GEMINI_API_KEY='')
    def test_guide_chat_api_asks_for_product_when_cart_request_is_ambiguous(self):
        response = self.client.post(reverse('core:guide_chat_api'), {'message': 'add pottery to cart'})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('Which product should I add?', data['answer'])
        self.assertIn('Clay Serving Bowl', data['answer'])
        self.assertIn('Handmade Water Pot', data['answer'])
        self.assertNotIn(CART_SESSION_KEY, self.client.session)

    @override_settings(GEMINI_API_KEY='')
    def test_guide_chat_api_adds_product_from_follow_up_context(self):
        product = Product.objects.get(slug='handmade-water-pot')
        first_response = self.client.post(reverse('core:guide_chat_api'), {'message': 'Tell me about Handmade Water Pot'})
        self.assertEqual(first_response.status_code, 200)

        follow_up = self.client.post(reverse('core:guide_chat_api'), {'message': 'add it to cart'})

        self.assertEqual(follow_up.status_code, 200)
        data = follow_up.json()
        self.assertIn('I added Handmade Water Pot to your cart', data['answer'])
        self.assertEqual(self.client.session[CART_SESSION_KEY], {str(product.pk): 1})

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
