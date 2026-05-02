from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from bookings.models import Experience
from core.models import SiteViewerSettings
from marketplace.models import Product
from village.models import Hut


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
        self.assertContains(response, 'Journal progress')
        self.assertContains(response, reverse('dashboard:journal'))
        self.assertContains(response, 'Enter Virtual Village')
        self.assertContains(response, 'Browse Cultural Products')

    def test_dashboard_renders_vendor_workspace_for_vendor_group(self):
        vendor_group = Group.objects.create(name='Vendor')
        user = User.objects.create_user(
            username='host@example.com',
            email='host@example.com',
            password='StrongPass12345!',
        )
        user.groups.add(vendor_group)
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vendor tools')
        self.assertContains(response, 'Manage Experiences')
        self.assertContains(response, reverse('dashboard:vendor'))

    def test_dashboard_renders_developer_workspace_for_staff(self):
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
        self.assertContains(response, 'Staff overview')
        self.assertContains(response, reverse('dashboard:admin_workspace'))

    def test_passport_requires_login(self):
        response = self.client.get(reverse('dashboard:journal'))

        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:journal')}")

    def test_passport_renders_huts_and_badges(self):
        user = User.objects.create_user(
            username='nila@example.com',
            email='nila@example.com',
            password='StrongPass12345!',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:journal'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/journal.html')
        self.assertContains(response, 'Cultural Journal')
        self.assertContains(response, 'Pottery Hut')
        self.assertContains(response, 'Clay Keeper')
        self.assertContains(response, 'Continue Hut')

    def test_legacy_passport_url_redirects_to_journal(self):
        response = self.client.get(reverse('dashboard:passport_legacy'))

        self.assertRedirects(response, reverse('dashboard:journal'), fetch_redirect_response=False)

    def test_host_workspace_requires_login(self):
        response = self.client.get(reverse('dashboard:host'))

        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:host')}")

    def test_host_workspace_blocks_normal_viewer(self):
        user = User.objects.create_user(
            username='viewer@example.com',
            email='viewer@example.com',
            password='StrongPass12345!',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:host'))

        self.assertEqual(response.status_code, 403)

    def test_vendor_workspace_renders_management_page(self):
        vendor_group = Group.objects.create(name='Vendor')
        user = User.objects.create_user(
            username='host@example.com',
            email='host@example.com',
            password='StrongPass12345!',
        )
        user.groups.add(vendor_group)
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:host'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/host.html')
        self.assertContains(response, 'Manage the cultural experiences you provide.')
        self.assertContains(response, 'Your listings and enquiries.')
        self.assertContains(response, reverse('dashboard:vendor_experience_create'))

    def test_vendor_can_submit_experience_for_admin_review(self):
        vendor_group = Group.objects.create(name='Vendor')
        user = User.objects.create_user(
            username='vendor@example.com',
            email='vendor@example.com',
            password='StrongPass12345!',
            first_name='Kavin',
        )
        user.groups.add(vendor_group)
        self.client.force_login(user)
        hut = Hut.objects.get(slug='pottery')

        response = self.client.post(reverse('dashboard:vendor_experience_create'), {
            'hut': str(hut.pk),
            'title': 'Village Clay Workshop',
            'slug': 'village-clay-workshop',
            'host': 'Kavin Studio',
            'duration': '2 hours',
            'price': '3500',
            'currency': 'LKR',
            'summary': 'A hands-on pottery session for small groups.',
            'includes_text': 'Clay preparation\nGuided shaping',
        })

        self.assertRedirects(response, reverse('dashboard:vendor'))
        experience = Experience.objects.get(slug='village-clay-workshop')
        self.assertEqual(experience.provider, user)
        self.assertFalse(experience.is_published)
        self.assertEqual(experience.status, Experience.STATUS_PREVIEW)
        self.assertEqual(experience.includes, ['Clay preparation', 'Guided shaping'])

    def test_normal_viewer_cannot_open_vendor_experience_form(self):
        user = User.objects.create_user(
            username='viewer@example.com',
            email='viewer@example.com',
            password='StrongPass12345!',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:vendor_experience_create'))

        self.assertEqual(response.status_code, 403)

    def test_admin_workspace_requires_login(self):
        response = self.client.get(reverse('dashboard:admin_workspace'))

        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:admin_workspace')}")

    def test_admin_workspace_blocks_normal_viewer(self):
        user = User.objects.create_user(
            username='viewer@example.com',
            email='viewer@example.com',
            password='StrongPass12345!',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:admin_workspace'))

        self.assertEqual(response.status_code, 403)

    def test_developer_admin_workspace_renders_approval_page(self):
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
        self.assertContains(response, 'Control center')
        self.assertContains(response, 'Whole-site snapshot.')
        self.assertContains(response, 'Choose what visitors see.')

    def test_admin_can_save_public_visibility_flags(self):
        SiteViewerSettings.get_solo()
        user = User.objects.create_user(
            username='staff@example.com',
            email='staff@example.com',
            password='StrongPass12345!',
            is_staff=True,
        )
        self.client.force_login(user)
        response = self.client.post(
            reverse('dashboard:admin_workspace'),
            {
                'admin_action': 'save_visibility',
            },
            follow=False,
        )
        self.assertRedirects(response, reverse('dashboard:admin_workspace'))
        settings_obj = SiteViewerSettings.get_solo()
        self.assertFalse(settings_obj.public_show_virtual_village)
        self.assertFalse(settings_obj.public_show_marketplace)

    def test_admin_can_publish_pending_experience(self):
        vendor_group = Group.objects.create(name='Vendor')
        vendor = User.objects.create_user(
            username='vendor-publish@example.com',
            email='vendor-publish@example.com',
            password='StrongPass12345!',
        )
        vendor.groups.add(vendor_group)
        hut = Hut.objects.get(slug='pottery')
        experience = Experience.objects.create(
            hut=hut,
            provider=vendor,
            slug='awaiting-publish-exp',
            title='Awaiting publish',
            host='River Studio',
            duration='90 minutes',
            price=4200,
            currency='LKR',
            summary='Pending summary for testers.',
            includes=['Clay intro'],
            is_published=False,
            status=Experience.STATUS_PREVIEW,
        )
        staff = User.objects.create_user(
            username='staff-publish@example.com',
            email='staff-publish@example.com',
            password='StrongPass12345!',
            is_staff=True,
        )
        self.client.force_login(staff)
        response = self.client.post(
            reverse('dashboard:admin_workspace'),
            {'admin_action': 'publish_experience', 'experience_id': str(experience.pk)},
            follow=False,
        )
        self.assertRedirects(response, reverse('dashboard:admin_workspace'))
        experience.refresh_from_db()
        self.assertTrue(experience.is_published)
        self.assertEqual(experience.status, Experience.STATUS_TAKING_REQUESTS)

    def test_admin_can_publish_pending_product(self):
        hut = Hut.objects.get(slug='pottery')
        product = Product.objects.create(
            hut=hut,
            slug='unpublished-clay-pin',
            name='Clay pin brooch',
            price=890,
            currency='LKR',
            summary='Test listing awaiting approval.',
            artisan='River Studio',
            materials='Clay',
            stock=4,
            is_published=False,
            status=Product.STATUS_AVAILABLE,
        )
        staff = User.objects.create_user(
            username='staff-prod@example.com',
            email='staff-prod@example.com',
            password='StrongPass12345!',
            is_staff=True,
        )
        self.client.force_login(staff)
        response = self.client.post(
            reverse('dashboard:admin_workspace'),
            {'admin_action': 'publish_product', 'product_id': str(product.pk)},
            follow=False,
        )
        self.assertRedirects(response, reverse('dashboard:admin_workspace'))
        product.refresh_from_db()
        self.assertTrue(product.is_published)
