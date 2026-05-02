from django.contrib.auth.models import Group, User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', DEBUG=True)
class SignupTests(TestCase):
    def test_signup_creates_inactive_user_and_sends_verification_email(self):
        response = self.client.post(reverse('accounts:signup'), {
            'first_name': 'Nila',
            'email': 'nila@example.com',
            'account_type': 'Viewer',
            'password1': 'StrongPass12345!',
            'password2': 'StrongPass12345!',
        })

        self.assertRedirects(response, reverse('accounts:verification_sent'), fetch_redirect_response=False)
        user = User.objects.get(email='nila@example.com')
        self.assertEqual(user.username, 'nila@example.com')
        self.assertFalse(user.is_active)
        self.assertTrue(user.groups.filter(name='Viewer').exists())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Verify your AerUla account', mail.outbox[0].subject)
        self.assertIn('/accounts/verify/', mail.outbox[0].body)
        verification_response = self.client.get(reverse('accounts:verification_sent'))
        self.assertContains(verification_response, 'Local verification link (development only)')

    def test_signup_rejects_duplicate_email(self):
        User.objects.create_user(
            username='nila@example.com',
            email='nila@example.com',
            password='StrongPass12345!',
        )

        response = self.client.post(reverse('accounts:signup'), {
            'first_name': 'Nila',
            'email': 'NILA@example.com',
            'account_type': 'Viewer',
            'password1': 'StrongPass12345!',
            'password2': 'StrongPass12345!',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'An account with this email already exists.')
        self.assertEqual(User.objects.filter(email__iexact='nila@example.com').count(), 1)

    def test_vendor_signup_assigns_vendor_group(self):
        response = self.client.post(reverse('accounts:signup'), {
            'first_name': 'Kavin',
            'email': 'vendor@example.com',
            'account_type': 'Vendor',
            'password1': 'StrongPass12345!',
            'password2': 'StrongPass12345!',
        })

        self.assertRedirects(response, reverse('accounts:verification_sent'), fetch_redirect_response=False)
        user = User.objects.get(email='vendor@example.com')
        self.assertTrue(user.groups.filter(name='Vendor').exists())
        self.assertTrue(Group.objects.filter(name='Vendor').exists())


class LoginTests(TestCase):
    def test_login_page_renders_signup_link(self):
        response = self.client.get(reverse('accounts:login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Continue your cultural journey.')
        self.assertContains(response, reverse('accounts:signup'))

    def test_inactive_user_cannot_login_before_verification(self):
        User.objects.create_user(
            username='nila@example.com',
            email='nila@example.com',
            password='StrongPass12345!',
            is_active=False,
        )

        response = self.client.post(reverse('accounts:login'), {
            'username': 'nila@example.com',
            'password': 'StrongPass12345!',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your account is not verified yet.')
        self.assertContains(response, reverse('accounts:resend_verification'))


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', DEBUG=True)
class ResendVerificationTests(TestCase):
    def test_resend_verification_sends_new_email_for_inactive_account(self):
        User.objects.create_user(
            username='nila@example.com',
            email='nila@example.com',
            password='StrongPass12345!',
            is_active=False,
        )

        response = self.client.post(reverse('accounts:resend_verification'), {
            'email': 'NILA@example.com',
        })

        self.assertRedirects(response, reverse('accounts:verification_sent'), fetch_redirect_response=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/accounts/verify/', mail.outbox[0].body)
        verification_response = self.client.get(reverse('accounts:verification_sent'))
        self.assertContains(verification_response, 'Local verification link (development only)')

    def test_resend_verification_does_not_send_for_active_account(self):
        User.objects.create_user(
            username='nila@example.com',
            email='nila@example.com',
            password='StrongPass12345!',
            is_active=True,
        )

        response = self.client.post(reverse('accounts:resend_verification'), {
            'email': 'nila@example.com',
        })

        self.assertRedirects(response, reverse('accounts:login'))
        self.assertEqual(len(mail.outbox), 0)


class EmailVerificationTests(TestCase):
    def test_valid_verification_link_activates_and_logs_in_user(self):
        user = User.objects.create_user(
            username='nila@example.com',
            email='nila@example.com',
            password='StrongPass12345!',
            is_active=False,
        )
        url = reverse('accounts:verify_email', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        response = self.client.get(url)

        self.assertRedirects(response, reverse('dashboard:index'))
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_invalid_verification_link_redirects_to_login(self):
        user = User.objects.create_user(
            username='nila@example.com',
            email='nila@example.com',
            password='StrongPass12345!',
            is_active=False,
        )
        url = reverse('accounts:verify_email', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': 'invalid-token',
        })

        response = self.client.get(url)

        self.assertRedirects(response, reverse('accounts:login'))
        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_already_verified_link_redirects_to_dashboard(self):
        user = User.objects.create_user(
            username='nila@example.com',
            email='nila@example.com',
            password='StrongPass12345!',
            is_active=False,
        )
        token = account_activation_token.make_token(user)
        user.is_active = True
        user.save(update_fields=['is_active'])
        url = reverse('accounts:verify_email', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })

        response = self.client.get(url)

        self.assertRedirects(response, reverse('accounts:login'))
        self.assertNotIn('_auth_user_id', self.client.session)
