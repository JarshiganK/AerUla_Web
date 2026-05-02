from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.roles import developer_required, is_developer, is_vendor, vendor_required
from bookings.forms import VendorExperienceForm
from bookings.models import BookingRequest, Experience
from core.models import SiteViewerSettings
from marketplace.models import Order, Product
from simulations.models import UserProgress
from village.models import Hut


@login_required
def index(request):
    user_is_vendor = is_vendor(request.user)
    user_is_developer = is_developer(request.user)

    context = {
        'is_vendor': user_is_vendor,
        'is_developer': user_is_developer,
        'journey_steps': [
            {
                'label': 'Explore',
                'title': 'Enter the Virtual Village',
                'description': 'Choose a cultural hut and start your next learning activity.',
                'action': 'Open Village',
                'url_name': 'village:index',
            },
            {
                'label': 'Learn',
                'title': 'Complete a Hut Activity',
                'description': 'Read the story, complete the hut activity, and save your badge.',
                'action': 'Continue Journey',
                'url_name': 'village:index',
            },
            {
                'label': 'Connect',
                'title': 'Browse Cultural Products',
                'description': 'Find marketplace items connected to the huts you are exploring.',
                'action': 'Browse Marketplace',
                'url_name': 'marketplace:index',
            },
        ],
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def cultural_journal(request):
    progress_by_hut = {
        progress.hut_id: progress
        for progress in UserProgress.objects.filter(user=request.user).select_related('hut')
    }
    journal_huts = [
        {
            'hut': hut,
            'completed': progress_by_hut.get(hut.id).completed if hut.id in progress_by_hut else False,
            'score': progress_by_hut.get(hut.id).score if hut.id in progress_by_hut else 'Pending',
        }
        for hut in Hut.objects.filter(is_active=True)
    ]
    completed_count = sum(item['completed'] for item in journal_huts)
    return render(
        request,
        'dashboard/journal.html',
        {
            'journal_huts': journal_huts,
            'completed_count': completed_count,
            'total_count': len(journal_huts),
        },
    )


@login_required
@vendor_required
def host_workspace(request):
    vendor_experiences = Experience.objects.filter(provider=request.user).select_related('hut')
    pending_booking_count = BookingRequest.objects.filter(
        experience__provider=request.user,
        status=BookingRequest.STATUS_PENDING,
    ).count()
    return render(
        request,
        'dashboard/host.html',
        {
            'host_metrics': [
                ('My experience listings', f'{vendor_experiences.count()} submitted'),
                ('My booking requests', f'{pending_booking_count} pending'),
                ('Marketplace products', f'{Product.objects.count()} catalogue items'),
            ],
            'vendor_experiences': vendor_experiences,
        },
    )


@login_required
@vendor_required
def vendor_experience_create(request):
    if request.method == 'POST':
        form = VendorExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.provider = request.user
            experience.save()
            messages.success(request, 'Submitted for admin approval—we will review your experience shortly.')
            return redirect('dashboard:vendor')
    else:
        initial = {}
        if request.user.first_name:
            initial['host'] = request.user.first_name
        form = VendorExperienceForm(initial=initial)

    return render(
        request,
        'dashboard/vendor_experience_form.html',
        {
            'form': form,
        },
    )


def _build_admin_analytics():
    User = get_user_model()
    return {
        'registered_users': User.objects.filter(is_active=True).count(),
        'published_experiences': Experience.objects.filter(is_published=True).count(),
        'pending_experiences': Experience.objects.filter(is_published=False).count(),
        'published_products': Product.objects.filter(is_published=True).count(),
        'pending_products': Product.objects.filter(is_published=False).count(),
        'pending_booking_requests': BookingRequest.objects.filter(status=BookingRequest.STATUS_PENDING).count(),
        'booking_requests_total': BookingRequest.objects.count(),
        'orders_total': Order.objects.count(),
        'hut_completions': UserProgress.objects.filter(completed=True).count(),
        'active_huts': Hut.objects.filter(is_active=True).count(),
    }


@login_required
@developer_required
def admin_workspace(request):
    if request.method == 'POST':
        action = request.POST.get('admin_action', '')
        settings_obj = SiteViewerSettings.get_solo()

        if action == 'save_visibility':
            settings_obj.public_show_virtual_village = request.POST.get('public_show_virtual_village') == 'on'
            settings_obj.public_show_marketplace = request.POST.get('public_show_marketplace') == 'on'
            settings_obj.public_show_experience_bookings = request.POST.get('public_show_experience_bookings') == 'on'
            settings_obj.public_show_cultural_guide = request.POST.get('public_show_cultural_guide') == 'on'
            settings_obj.save()
            messages.success(request, 'What visitors see on the public site is updated.')
            return redirect('dashboard:admin_workspace')

        if action == 'publish_experience':
            experience_id = request.POST.get('experience_id')
            if experience_id and experience_id.isdigit():
                experience = Experience.objects.filter(pk=int(experience_id), is_published=False).first()
                if experience:
                    experience.is_published = True
                    experience.status = Experience.STATUS_TAKING_REQUESTS
                    experience.save(update_fields=['is_published', 'status', 'updated_at'])
                    messages.success(request, f'Approved and published "{experience.title}".')
                    return redirect('dashboard:admin_workspace')

        if action == 'publish_product':
            product_id = request.POST.get('product_id')
            if product_id and product_id.isdigit():
                product = Product.objects.filter(pk=int(product_id), is_published=False).first()
                if product:
                    product.is_published = True
                    product.save(update_fields=['is_published', 'updated_at'])
                    messages.success(request, f'Published product "{product.name}".')
                    return redirect('dashboard:admin_workspace')

        messages.error(request, 'That admin action could not be completed.')
        return redirect('dashboard:admin_workspace')

    pending_experiences = Experience.objects.filter(is_published=False).select_related('hut', 'provider').order_by(
        '-created_at'
    )
    pending_products = Product.objects.filter(is_published=False).select_related('hut').order_by('-created_at')

    return render(
        request,
        'dashboard/admin_workspace.html',
        {
            'analytics': _build_admin_analytics(),
            'pending_experiences': pending_experiences,
            'pending_products': pending_products,
            'approval_queues': [
                (
                    'Experiences awaiting approval',
                    f'{pending_experiences.count()} pending',
                ),
                ('Products awaiting listing', f'{pending_products.count()} pending'),
                (
                    'Booking requests (pending)',
                    f'{BookingRequest.objects.filter(status=BookingRequest.STATUS_PENDING).count()} open',
                ),
                ('Active huts', f'{Hut.objects.filter(is_active=True).count()} live'),
            ],
        },
    )
