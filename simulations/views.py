from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone

from village.models import Hut

from .models import QuizQuestion, SimulationStep, UserProgress


def index(request):
    first_available = Hut.objects.filter(status=Hut.STATUS_AVAILABLE, is_active=True).first()
    if first_available is None:
        raise Http404('Simulation not found')
    return redirect('simulations:preview', slug=first_available.slug)


def preview(request, slug):
    try:
        hut = Hut.objects.get(slug=slug, is_active=True)
    except Hut.DoesNotExist:
        raise Http404('Simulation not found')

    ordered_steps = list(SimulationStep.objects.filter(hut=hut).order_by('correct_order'))
    shuffled_steps = list(SimulationStep.objects.filter(hut=hut).order_by('preview_order'))
    return render(
        request,
        'simulations/preview.html',
        {
            'hut': hut,
            'ordered_steps': list(enumerate(ordered_steps, start=1)),
            'shuffled_steps': shuffled_steps,
        },
    )


def quiz(request, slug):
    try:
        hut = Hut.objects.get(slug=slug, is_active=True)
    except Hut.DoesNotExist:
        raise Http404('Quiz not found')

    quiz_question = QuizQuestion.objects.filter(hut=hut).prefetch_related('options').first()
    if quiz_question is None:
        raise Http404('Quiz not found')

    selected_answer = ''
    is_correct = None
    if request.method == 'POST':
        selected_answer = request.POST.get('answer', '')
        correct_option = quiz_question.options.filter(is_correct=True).first()
        is_correct = correct_option is not None and selected_answer == correct_option.text
        if is_correct and request.user.is_authenticated:
            UserProgress.objects.update_or_create(
                user=request.user,
                hut=hut,
                defaults={'completed': True, 'score': 100, 'completed_at': timezone.now()},
            )

    return render(
        request,
        'simulations/quiz.html',
        {
            'hut': hut,
            'quiz_question': quiz_question,
            'selected_answer': selected_answer,
            'is_correct': is_correct,
        },
    )
