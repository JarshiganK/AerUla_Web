from django.test import TestCase
from django.urls import reverse

from .models import BookingRequest


class BookingPageTests(TestCase):
    def test_booking_index_renders_experiences(self):
        response = self.client.get(reverse('bookings:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/index.html')
        self.assertContains(response, 'Book experiences rooted in each hut.')
        self.assertContains(response, 'Pottery Workshop Visit')
        self.assertContains(response, 'Palmyrah Weaving Session')

    def test_booking_detail_renders_request_preview(self):
        response = self.client.get(reverse('bookings:detail', kwargs={'slug': 'pottery-workshop'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/detail.html')
        self.assertContains(response, 'Pottery Workshop Visit')
        self.assertContains(response, 'Kopay Pottery Collective')
        self.assertContains(response, 'Request a booking')
        self.assertContains(response, reverse('bookings:request', kwargs={'slug': 'pottery-workshop'}))

    def test_booking_request_page_renders_form(self):
        response = self.client.get(reverse('bookings:request', kwargs={'slug': 'pottery-workshop'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/request.html')
        self.assertContains(response, 'Booking request')
        self.assertContains(response, 'Preferred date')
        self.assertContains(response, 'Submit Request')

    def test_booking_request_post_renders_received_state(self):
        response = self.client.post(reverse('bookings:request', kwargs={'slug': 'pottery-workshop'}), {
            'preferred_date': '2026-05-20',
            'guests': '2',
            'notes': 'Morning preferred',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thank you')
        self.assertEqual(BookingRequest.objects.count(), 1)
        self.assertEqual(BookingRequest.objects.get().guests, 2)

    def test_unknown_booking_returns_404(self):
        response = self.client.get(reverse('bookings:detail', kwargs={'slug': 'missing'}))

        self.assertEqual(response.status_code, 404)

    def test_unknown_booking_request_returns_404(self):
        response = self.client.get(reverse('bookings:request', kwargs={'slug': 'missing'}))

        self.assertEqual(response.status_code, 404)
