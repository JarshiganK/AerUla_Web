from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page_renders_design_system_content(self):
        response = self.client.get(reverse('core:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Explore Sri Lankan heritage')
        self.assertContains(response, 'Enter Virtual Village')
        self.assertContains(response, 'Browse Marketplace')
        self.assertContains(response, 'Passport progress')


class PlaceholderRouteTests(TestCase):
    def test_placeholder_app_routes_render(self):
        routes = {
            'accounts:index': 'AerUla accounts module is ready.',
            'bookings:index': 'AerUla bookings module is ready.',
            'dashboard:index': 'AerUla dashboard module is ready.',
            'marketplace:index': 'AerUla marketplace module is ready.',
            'simulations:index': 'AerUla simulations module is ready.',
            'village:index': 'AerUla virtual village module is ready.',
        }

        for route_name, expected_text in routes.items():
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected_text)
