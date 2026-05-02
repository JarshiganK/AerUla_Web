from django.http import Http404
from django.shortcuts import redirect, render

from village.content import HUTS, get_hut


def index(request):
    first_available = next((hut for hut in HUTS if hut['status'] == 'available'), HUTS[0])
    return redirect('simulations:preview', slug=first_available['slug'])


def preview(request, slug):
    hut = get_hut(slug)
    if hut is None:
        raise Http404('Simulation not found')

    return render(
        request,
        'simulations/preview.html',
        {
            'hut': hut,
            'ordered_steps': list(enumerate(hut['steps'], start=1)),
            'shuffled_steps': _preview_order(hut['steps']),
        },
    )


def quiz(request, slug):
    hut = get_hut(slug)
    if hut is None:
        raise Http404('Quiz not found')

    selected_answer = ''
    is_correct = None
    if request.method == 'POST':
        selected_answer = request.POST.get('answer', '')
        is_correct = selected_answer == hut['quiz_options'][0]

    return render(
        request,
        'simulations/quiz.html',
        {
            'hut': hut,
            'selected_answer': selected_answer,
            'is_correct': is_correct,
        },
    )


def _preview_order(steps):
    if len(steps) < 3:
        return steps
    return steps[1::2] + steps[::2]
