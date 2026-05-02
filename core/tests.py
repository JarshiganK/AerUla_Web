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
        self.assertContains(response, 'Real cultural references')
        self.assertContains(response, 'Tradtional_Sri_Lankan_Pottery.jpg')


class RouteTests(TestCase):
    def test_accounts_index_redirects_to_login(self):
        response = self.client.get(reverse('accounts:index'))

        self.assertRedirects(response, reverse('accounts:login'))
