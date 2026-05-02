from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from .content import HUTS, get_hut


def index(request):
    available_count = sum(hut['status'] == 'available' for hut in HUTS)
    huts = [_with_url(hut) for hut in HUTS]
    context = {
        'huts': huts,
        'available_count': available_count,
        'total_count': len(huts),
        'featured_hut': huts[0],
    }
    return render(request, 'village/index.html', context)


def detail(request, slug):
    hut = get_hut(slug)
    if hut is None:
        raise Http404('Hut not found')

    hut = _with_url(hut)
    other_huts = [_with_url(item) for item in HUTS if item['slug'] != slug]
    return render(
        request,
        'village/detail.html',
        {
            'hut': hut,
            'other_huts': other_huts,
        },
    )


def _with_url(hut):
    return {
        **hut,
        'url': reverse('village:detail', kwargs={'slug': hut['slug']}),
    }
