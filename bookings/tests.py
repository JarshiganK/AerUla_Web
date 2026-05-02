from django.test import TestCase
from django.urls import reverse


class BookingPageTests(TestCase):
    def test_booking_index_renders_experiences(self):
        response = self.client.get(reverse('bookings:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/index.html')
        self.assertContains(response, 'Reserve cultural experiences connected to the huts.')
        self.assertContains(response, 'Pottery Workshop Visit')
        self.assertContains(response, 'Palmyrah Weaving Session')

    def test_booking_detail_renders_request_preview(self):
        response = self.client.get(reverse('bookings:detail', kwargs={'slug': 'pottery-workshop'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/detail.html')
        self.assertContains(response, 'Pottery Workshop Visit')
        self.assertContains(response, 'Kopay Pottery Collective')
        self.assertContains(response, 'Request Booking Preview')

    def test_unknown_booking_returns_404(self):
        response = self.client.get(reverse('bookings:detail', kwargs={'slug': 'missing'}))

        self.assertEqual(response.status_code, 404)
