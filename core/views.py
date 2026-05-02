from django.shortcuts import render

from village.models import Hut


def home(request):
    featured_huts = Hut.objects.filter(is_active=True)
    return render(request, 'core/home.html', {'featured_huts': featured_huts})
