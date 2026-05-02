from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from village.content import HUTS


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
    passport_huts = [
        {
            **hut,
            'completed': False,
            'score': 'Pending',
        }
        for hut in HUTS
    ]
    return render(
        request,
        'dashboard/passport.html',
        {
            'passport_huts': passport_huts,
            'completed_count': 0,
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
                ('Experience listings', '3 drafts'),
                ('Booking requests', '2 pending'),
                ('Products', '5 catalogue items'),
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
                ('Products', '4 pending'),
                ('Bookings', '3 review items'),
                ('Quizzes', '5 content checks'),
            ],
        },
    )
