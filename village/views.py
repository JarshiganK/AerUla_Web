from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from marketplace.models import Product
from simulations.models import QuizQuestion, SimulationStep, UserProgress

from .models import Hut


def index(request):
    huts = [_with_url(hut) for hut in Hut.objects.filter(is_active=True)]
    available_count = sum(hut.status == Hut.STATUS_AVAILABLE for hut in huts)
    context = {
        'huts': huts,
        'available_count': available_count,
        'total_count': len(huts),
        'featured_hut': huts[0] if huts else None,
    }
    return render(request, 'village/index.html', context)


def detail(request, slug):
    try:
        hut = Hut.objects.get(slug=slug, is_active=True)
    except Hut.DoesNotExist:
        raise Http404('Hut not found')

    hut = _with_url(hut)
    steps = SimulationStep.objects.filter(hut=hut).order_by('correct_order')
    quiz_question = QuizQuestion.objects.filter(hut=hut).prefetch_related('options').first()
    related_products = Product.objects.filter(hut=hut, is_published=True)[:2]
    other_huts = [_with_url(item) for item in Hut.objects.filter(is_active=True).exclude(slug=slug)]
    progress = None
    if request.user.is_authenticated:
        progress = UserProgress.objects.filter(user=request.user, hut=hut).first()

    return render(
        request,
        'village/detail.html',
        {
            'hut': hut,
            'steps': steps,
            'quiz_question': quiz_question,
            'related_products': related_products,
            'other_huts': other_huts,
            'progress': progress,
        },
    )


def _with_url(hut):
    hut.url = reverse('village:detail', kwargs={'slug': hut.slug})
    return hut
