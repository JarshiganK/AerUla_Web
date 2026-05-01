from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


class DashboardTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard:index'))

        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:index')}")

    def test_dashboard_renders_tourist_journey_for_authenticated_user(self):
        user = User.objects.create_user(
            username='nila@example.com',
            email='nila@example.com',
            password='StrongPass12345!',
            first_name='Nila',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, Nila.')
        self.assertContains(response, 'Passport progress')
        self.assertContains(response, 'Enter Virtual Village')
        self.assertContains(response, 'Browse Cultural Products')

    def test_dashboard_renders_host_workspace_for_host_group(self):
        host_group = Group.objects.create(name='Host')
        user = User.objects.create_user(
            username='host@example.com',
            email='host@example.com',
            password='StrongPass12345!',
        )
        user.groups.add(host_group)
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Host tools')
        self.assertContains(response, 'Experience listings')

    def test_dashboard_renders_admin_workspace_for_staff(self):
        user = User.objects.create_user(
            username='admin@example.com',
            email='admin@example.com',
            password='StrongPass12345!',
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin tools')
        self.assertContains(response, 'Approvals')
