from django.test import TestCase
from django.urls import reverse


class MarketplaceTests(TestCase):
    def test_marketplace_index_renders_catalogue(self):
        response = self.client.get(reverse('marketplace:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketplace/index.html')
        self.assertContains(response, 'Products connected to the cultural village journey.')
        self.assertContains(response, 'Clay Serving Bowl')
        self.assertContains(response, 'Woven Palmyrah Basket')
        self.assertContains(response, 'All products')

    def test_marketplace_can_filter_by_hut(self):
        response = self.client.get(reverse('marketplace:index'), {'hut': 'pottery'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clay Serving Bowl')
        self.assertContains(response, 'Handmade Water Pot')
        self.assertNotContains(response, 'Woven Palmyrah Basket')

    def test_product_detail_renders_conversion_actions(self):
        response = self.client.get(reverse('marketplace:detail', kwargs={'slug': 'clay-serving-bowl'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketplace/detail.html')
        self.assertContains(response, 'Clay Serving Bowl')
        self.assertContains(response, 'Nallur Clay Studio')
        self.assertContains(response, 'Add to Cart Preview')
        self.assertContains(response, reverse('marketplace:cart'))
        self.assertContains(response, reverse('bookings:index'))

    def test_cart_page_renders_checkout_action(self):
        response = self.client.get(reverse('marketplace:cart'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketplace/cart.html')
        self.assertContains(response, 'Review selected cultural products.')
        self.assertContains(response, 'Continue to Checkout')

    def test_checkout_page_renders_order_preview(self):
        response = self.client.get(reverse('marketplace:checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketplace/checkout.html')
        self.assertContains(response, 'Place order preview.')
        self.assertContains(response, 'AER-MVP-0001')

    def test_unknown_product_returns_404(self):
        response = self.client.get(reverse('marketplace:detail', kwargs={'slug': 'missing'}))

        self.assertEqual(response.status_code, 404)
