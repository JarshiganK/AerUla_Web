from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.roles import developer_required, is_developer, is_vendor, vendor_required
from bookings.forms import VendorExperienceForm
from bookings.models import BookingRequest, Experience
from marketplace.models import Product
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
                'description': 'Read the story, finish the verified simulation, and record your badge.',
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
def passport(request):
    progress_by_hut = {
        progress.hut_id: progress
        for progress in UserProgress.objects.filter(user=request.user).select_related('hut')
    }
    passport_huts = [
        {
            'hut': hut,
            'completed': progress_by_hut.get(hut.id).completed if hut.id in progress_by_hut else False,
            'score': progress_by_hut.get(hut.id).score if hut.id in progress_by_hut else 'Pending',
        }
        for hut in Hut.objects.filter(is_active=True)
    ]
    completed_count = sum(item['completed'] for item in passport_huts)
    return render(
        request,
        'dashboard/passport.html',
        {
            'passport_huts': passport_huts,
            'completed_count': completed_count,
            'total_count': len(passport_huts),
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
            messages.success(request, 'Your experience was submitted for admin review.')
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


@login_required
@developer_required
def admin_workspace(request):
    return render(
        request,
        'dashboard/admin_workspace.html',
        {
            'approval_queues': [
                (
                    'Vendor experiences',
                    f'{Experience.objects.filter(provider__isnull=False, is_published=False).count()} pending',
                ),
                ('Products', f'{Product.objects.filter(is_published=False).count()} pending'),
                ('Bookings', f'{BookingRequest.objects.filter(status=BookingRequest.STATUS_PENDING).count()} review items'),
                ('Huts', f'{Hut.objects.filter(is_active=True).count()} published'),
            ],
        },
    )
