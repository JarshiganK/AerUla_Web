from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from bookings.models import BookingRequest, Experience
from marketplace.models import Product
from simulations.models import UserProgress
from simulations.models import QuizQuestion
from village.models import Hut


@login_required
def index(request):
    groups = set(request.user.groups.values_list('name', flat=True))
    is_host = 'Host' in groups or 'host' in groups
    is_admin = request.user.is_staff or request.user.is_superuser

    context = {
        'is_host': is_host,
        'is_admin': is_admin,
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
                'description': 'Read the story, finish the mini simulation, and answer the quiz.',
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
def host_workspace(request):
    return render(
        request,
        'dashboard/host.html',
        {
            'host_metrics': [
                ('Experience listings', f'{Experience.objects.count()} active'),
                ('Booking requests', f'{BookingRequest.objects.filter(status=BookingRequest.STATUS_PENDING).count()} pending'),
                ('Products', f'{Product.objects.count()} catalogue items'),
            ],
        },
    )


@login_required
def admin_workspace(request):
    return render(
        request,
        'dashboard/admin_workspace.html',
        {
            'approval_queues': [
                ('Hosts', '2 pending'),
                ('Products', f'{Product.objects.filter(is_published=False).count()} pending'),
                ('Bookings', f'{BookingRequest.objects.filter(status=BookingRequest.STATUS_PENDING).count()} review items'),
                ('Quizzes', f'{QuizQuestion.objects.count()} content checks'),
                ('Huts', f'{Hut.objects.filter(is_active=True).count()} published'),
            ],
        },
    )
