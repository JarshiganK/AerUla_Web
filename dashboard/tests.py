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
        self.assertContains(response, reverse('dashboard:passport'))
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
        self.assertContains(response, 'Manage Listings')
        self.assertContains(response, reverse('dashboard:host'))

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
        self.assertContains(response, reverse('dashboard:admin_workspace'))

    def test_passport_requires_login(self):
        response = self.client.get(reverse('dashboard:passport'))

        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:passport')}")

    def test_passport_renders_huts_and_badges(self):
        user = User.objects.create_user(
            username='nila@example.com',
            email='nila@example.com',
            password='StrongPass12345!',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:passport'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/passport.html')
        self.assertContains(response, 'Cultural Passport')
        self.assertContains(response, 'Pottery Hut')
        self.assertContains(response, 'Clay Keeper')
        self.assertContains(response, 'Continue Hut')

    def test_host_workspace_requires_login(self):
        response = self.client.get(reverse('dashboard:host'))

        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:host')}")

    def test_host_workspace_renders_management_page(self):
        user = User.objects.create_user(
            username='host@example.com',
            email='host@example.com',
            password='StrongPass12345!',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:host'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/host.html')
        self.assertContains(response, 'Manage experiences, products, and availability.')
        self.assertContains(response, 'Booking requests')

    def test_admin_workspace_requires_login(self):
        response = self.client.get(reverse('dashboard:admin_workspace'))

        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:admin_workspace')}")

    def test_admin_workspace_renders_approval_page(self):
        user = User.objects.create_user(
            username='admin@example.com',
            email='admin@example.com',
            password='StrongPass12345!',
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:admin_workspace'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/admin_workspace.html')
        self.assertContains(response, 'Review approvals, content, and platform activity.')
        self.assertContains(response, 'Quizzes')
