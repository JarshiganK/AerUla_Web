from django.http import Http404
from django.shortcuts import render

from .content import EXPERIENCES, get_experience


def index(request):
    return render(
        request,
        'bookings/index.html',
        {
            'experiences': EXPERIENCES,
            'experience_count': len(EXPERIENCES),
        },
    )


def detail(request, slug):
    experience = get_experience(slug)
    if experience is None:
        raise Http404('Experience not found')

    return render(
        request,
        'bookings/detail.html',
        {
            'experience': experience,
        },
    )
