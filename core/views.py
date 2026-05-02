from django.shortcuts import render
from django.http import JsonResponse

from village.models import Hut

from .services import answer_guide_question, build_ai_guide, build_chat_messages


def home(request):
    featured_huts = Hut.objects.filter(is_active=True)
    guide_context = build_ai_guide(None)
    return render(
        request,
        'core/home.html',
        {
            'featured_huts': featured_huts,
            'guide_url': guide_context['guide_url'],
            'guide_prompt_links': guide_context['quick_prompts'],
        },
    )


def guide(request):
    if request.method == 'POST':
        query = request.POST.get('message', '').strip()
        if query:
            history = request.session.get('guide_chat_history', [])
            response = answer_guide_question(query, history=history)
            history.append({'user': query, 'assistant': response['answer']})
            request.session['guide_chat_history'] = history[-6:]
            request.session.modified = True

    if request.GET.get('clear') == '1':
        request.session.pop('guide_chat_history', None)

    prompt_query = request.GET.get('q', '').strip()
    chat_history = request.session.get('guide_chat_history', [])
    active_query = prompt_query

    if prompt_query and request.method == 'GET' and request.GET.get('clear') != '1':
        response = answer_guide_question(prompt_query, history=chat_history)
        chat_history = chat_history + [{'user': prompt_query, 'assistant': response['answer']}]

    guide_context = build_ai_guide(active_query)
    guide_context['chat_messages'] = build_chat_messages(chat_history)
    guide_context['current_message'] = active_query
    return render(request, 'core/guide.html', guide_context)


def guide_chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    action = request.POST.get('action', '').strip()
    if action == 'clear':
        request.session.pop('guide_chat_history', None)
        request.session.modified = True
        return JsonResponse(
            {
                'cleared': True,
                'messages': build_chat_messages([]),
            }
        )

    query = request.POST.get('message', '').strip()
    if not query:
        return JsonResponse({'error': 'Message is required'}, status=400)

    history = request.session.get('guide_chat_history', [])
    response = answer_guide_question(query, history=history)
    history.append({'user': query, 'assistant': response['answer'], 'sources': response['sources']})
    request.session['guide_chat_history'] = history[-6:]
    request.session.modified = True

    return JsonResponse(
        {
            'message': query,
            'answer': response['answer'],
            'sources': response['sources'],
            'messages': build_chat_messages(history),
        }
    )
