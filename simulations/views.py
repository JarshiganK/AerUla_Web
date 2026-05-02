import json

from django.http import Http404, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from village.models import Hut

from .models import QuizQuestion, UserProgress


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

    progress = None
    if request.user.is_authenticated:
        progress = UserProgress.objects.filter(user=request.user, hut=hut).first()
    get_token(request)

    return render(
        request,
        'simulations/preview.html',
        {
            'hut': hut,
            'progress': progress,
        },
    )


@require_POST
def complete(request, slug):
    try:
        hut = Hut.objects.get(slug=slug, is_active=True)
    except Hut.DoesNotExist:
        raise Http404('Simulation not found')

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid simulation payload.'}, status=400)

    try:
        watched_seconds = float(payload.get('watched_seconds', 0))
        coverage_degrees = int(payload.get('coverage_degrees', 0))
    except (TypeError, ValueError):
        return JsonResponse({'error': '360 simulation progress contains invalid values.'}, status=400)

    visited_hotspots = payload.get('hotspots', [])
    if not isinstance(visited_hotspots, list):
        return JsonResponse({'error': '360 hotspot progress is required.'}, status=400)

    scene = hut.simulation_360
    required_hotspots = {hotspot['id'] for hotspot in scene['hotspots']}
    visited_hotspots = {str(hotspot_id) for hotspot_id in visited_hotspots}
    valid_hotspots = visited_hotspots.intersection(required_hotspots)

    duration_required = scene['duration_required']
    coverage_required = scene['coverage_required']
    watched_score = min(watched_seconds / duration_required, 1) * 40
    coverage_score = min(coverage_degrees / coverage_required, 1) * 30
    hotspot_score = (
        (len(valid_hotspots) / len(required_hotspots)) * 30
        if required_hotspots
        else 30
    )
    score = round(watched_score + coverage_score + hotspot_score)
    simulation_completed = (
        watched_seconds >= duration_required
        and coverage_degrees >= coverage_required
        and valid_hotspots == required_hotspots
    )

    if request.user.is_authenticated:
        progress, _ = UserProgress.objects.get_or_create(user=request.user, hut=hut)
        progress.simulation_completed = progress.simulation_completed or simulation_completed
        progress.simulation_score = max(progress.simulation_score, score)
        if progress.quiz_completed and progress.simulation_completed:
            progress.completed = True
            progress.score = 100
            progress.completed_at = progress.completed_at or timezone.now()
        elif progress.simulation_completed:
            progress.score = max(progress.score, 50)
        progress.save(
            update_fields=[
                'simulation_completed',
                'simulation_score',
                'completed',
                'score',
                'completed_at',
                'updated_at',
            ]
        )

    return JsonResponse(
        {
            'score': score,
            'completed': simulation_completed,
            'quiz_url': reverse('simulations:quiz', kwargs={'slug': hut.slug}),
            'message': (
                '360 simulation verified. Take the quiz to record the badge.'
                if simulation_completed
                else 'Keep watching, looking around, and inspecting the required points.'
            ),
        }
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
    progress = None
    if request.user.is_authenticated:
        progress = UserProgress.objects.filter(user=request.user, hut=hut).first()

    if request.method == 'POST':
        selected_answer = request.POST.get('answer', '')
        correct_option = quiz_question.options.filter(is_correct=True).first()
        is_correct = correct_option is not None and selected_answer == correct_option.text
        if is_correct and request.user.is_authenticated:
            progress, _ = UserProgress.objects.get_or_create(user=request.user, hut=hut)
            progress.quiz_completed = True
            if progress.simulation_completed:
                progress.completed = True
                progress.score = 100
                progress.completed_at = progress.completed_at or timezone.now()
            else:
                progress.score = max(progress.score, 50)
            progress.save(
                update_fields=['quiz_completed', 'completed', 'score', 'completed_at', 'updated_at']
            )

    return render(
        request,
        'simulations/quiz.html',
        {
            'hut': hut,
            'quiz_question': quiz_question,
            'selected_answer': selected_answer,
            'is_correct': is_correct,
            'progress': progress,
        },
    )
