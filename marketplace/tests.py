from django.test import TestCase
from django.urls import reverse

from .models import Order


class MarketplaceTests(TestCase):
    def test_marketplace_index_renders_catalogue(self):
        response = self.client.get(reverse('marketplace:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketplace/index.html')
        self.assertContains(response, 'Products connected to the cultural village journey.')
        self.assertContains(response, 'Clay Serving Bowl')
        self.assertContains(response, 'Woven Palmyrah Basket')
        self.assertContains(response, 'All products')
        self.assertContains(response, 'Buy Now')
        self.assertContains(response, 'Ask Guide')
        self.assertContains(response, 'Tell me about Clay Serving Bowl')

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
        self.assertContains(response, 'Add to Cart')
        self.assertContains(response, 'Buy Now')
        self.assertContains(response, 'Ask Guide')
        self.assertContains(response, reverse('marketplace:add_to_cart', kwargs={'slug': 'clay-serving-bowl'}))
        self.assertContains(response, f"{reverse('marketplace:add_to_cart', kwargs={'slug': 'clay-serving-bowl'})}?next=checkout")
        self.assertContains(response, reverse('bookings:index'))

    def test_add_to_cart_stores_product_in_session(self):
        response = self.client.get(reverse('marketplace:add_to_cart', kwargs={'slug': 'clay-serving-bowl'}))

        self.assertRedirects(response, reverse('marketplace:cart'))
        self.assertTrue(self.client.session['marketplace_cart'])

    def test_buy_now_adds_product_and_redirects_to_checkout(self):
        response = self.client.get(
            reverse('marketplace:add_to_cart', kwargs={'slug': 'clay-serving-bowl'}),
            {'next': 'checkout'},
        )

        self.assertRedirects(response, reverse('marketplace:checkout'))
        self.assertTrue(self.client.session['marketplace_cart'])

    def test_cart_page_renders_checkout_action(self):
        self.client.get(reverse('marketplace:add_to_cart', kwargs={'slug': 'clay-serving-bowl'}))
        response = self.client.get(reverse('marketplace:cart'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketplace/cart.html')
        self.assertContains(response, 'Review selected cultural products.')
        self.assertContains(response, 'Continue to Checkout')

    def test_checkout_redirects_to_cart_when_cart_is_empty(self):
        response = self.client.get(reverse('marketplace:checkout'))

        self.assertRedirects(response, reverse('marketplace:cart'))

    def test_checkout_page_creates_order(self):
        self.client.get(reverse('marketplace:add_to_cart', kwargs={'slug': 'clay-serving-bowl'}))
        response = self.client.get(reverse('marketplace:checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketplace/checkout.html')
        self.assertContains(response, 'Place your order.')

        response = self.client.post(reverse('marketplace:checkout'), {
            'customer_name': 'Nila',
            'customer_email': 'nila@example.com',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order placed')
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().items.count(), 1)

    def test_unknown_product_returns_404(self):
        response = self.client.get(reverse('marketplace:detail', kwargs={'slug': 'missing'}))

        self.assertEqual(response.status_code, 404)

    def test_unknown_add_to_cart_returns_404(self):
        response = self.client.get(reverse('marketplace:add_to_cart', kwargs={'slug': 'missing'}))

        self.assertEqual(response.status_code, 404)
