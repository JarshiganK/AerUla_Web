from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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
