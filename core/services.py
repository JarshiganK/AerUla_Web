import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.urls import reverse

from marketplace.models import Product
from simulations.models import QuizQuestion, SimulationStep
from village.models import Hut


STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'ask', 'about', 'by', 'for', 'guide', 'how', 'is', 'me', 'of', 'or', 'the',
    'to', 'what', 'when', 'where', 'which', 'who', 'why', 'with', 'you', 'your', 'tell', 'more', 'this', 'that',
}

QUICK_PROMPTS = [
    'What does the pottery hut teach?',
    'How is palmyrah used in Jaffna culture?',
    'What real experience matches the fishing hut?',
    'How does the AI guide use the village content?',
]

MAX_CHAT_TURNS = 6
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
GEMINI_SYSTEM_INSTRUCTION = (
    'You are the AerUla cultural guide. Help visitors explore Sri Lankan traditions, huts, products, '
    'simulations, and booking links. Keep answers concise, friendly, and grounded in the supplied AerUla '
    'context. If the context does not fully answer the question, say what is known and suggest the best next '
    'AerUla page to open.'
)


def build_ai_guide(query: str | None):
    normalized_query = (query or '').strip()
    corpus = list(_build_corpus())
    ranked_sources = _rank_sources(corpus, normalized_query)

    if normalized_query and not ranked_sources:
        ranked_sources = _default_sources()

    if not normalized_query:
        ranked_sources = _default_sources()

    answer = _compose_answer(normalized_query, ranked_sources)
    return {
        'query': normalized_query,
        'answer': answer,
        'sources': ranked_sources,
        'quick_prompts': _build_quick_prompt_links(),
        'guide_url': reverse('core:guide'),
    }


def build_chat_messages(history):
    messages = []
    for turn in history[-MAX_CHAT_TURNS:]:
        user_message = (turn.get('user') or '').strip()
        assistant_message = (turn.get('assistant') or '').strip()
        if user_message:
            messages.append({'role': 'user', 'text': user_message})
        if assistant_message:
            messages.append({'role': 'assistant', 'text': assistant_message})

    if not messages:
        messages.append({
            'role': 'assistant',
            'text': 'Ask me about a hut, a product, a tradition, or a real experience. I will answer from AerUla content.',
        })

    return messages


def answer_guide_question(query, history=None):
    guide_context = build_ai_guide(query)
    sources = [
        {
            'title': source['title'],
            'summary': source['summary'],
            'url': source['url'],
            'source_label': source['source_label'],
            'badge': source['badge'],
            'extra': source['extra'],
        }
        for source in guide_context['sources']
    ]

    gemini_answer = _generate_gemini_answer(query, sources, history or [])
    if gemini_answer:
        answer = gemini_answer
        mode = 'gemini'
    else:
        answer = guide_context['answer']
        mode = 'retrieval'

    return {
        'answer': answer,
        'sources': sources,
        'quick_prompts': guide_context['quick_prompts'],
        'guide_url': guide_context['guide_url'],
        'mode': mode,
        'model': getattr(settings, 'GEMINI_MODEL', ''),
    }


def _build_corpus():
    huts = Hut.objects.filter(is_active=True).order_by('display_order', 'name')
    products = Product.objects.filter(is_published=True).select_related('hut').order_by('display_order', 'name')
    steps = SimulationStep.objects.select_related('hut').order_by('hut__display_order', 'correct_order')
    quizzes = QuizQuestion.objects.select_related('hut').order_by('hut__display_order', 'id')

    for hut in huts:
        yield {
            'type': 'hut',
            'title': hut.name,
            'text': ' '.join([hut.short_name, hut.summary, hut.activity, hut.story, hut.badge_title]),
            'summary': hut.summary,
            'url': reverse('village:detail', kwargs={'slug': hut.slug}),
            'source_label': 'Village hut',
            'badge': hut.badge_title,
            'extra': hut.activity,
        }

    for product in products:
        yield {
            'type': 'product',
            'title': product.name,
            'text': ' '.join([product.name, product.summary, product.artisan, product.materials, product.hut_name]),
            'summary': product.summary,
            'url': reverse('marketplace:detail', kwargs={'slug': product.slug}),
            'source_label': 'Marketplace product',
            'badge': product.status_label,
            'extra': f'{product.formatted_price} from {product.hut_name}',
        }

    for step in steps:
        yield {
            'type': 'step',
            'title': f'{step.hut.name} learning step',
            'text': ' '.join([step.hut.name, step.text]),
            'summary': step.text,
            'url': reverse('village:detail', kwargs={'slug': step.hut.slug}),
            'source_label': 'Simulation step',
            'badge': step.hut.badge_title,
            'extra': step.hut.activity,
        }

    for question in quizzes:
        yield {
            'type': 'quiz',
            'title': f'{question.hut.name} quiz question',
            'text': ' '.join([question.hut.name, question.question]),
            'summary': question.question,
            'url': reverse('village:detail', kwargs={'slug': question.hut.slug}),
            'source_label': 'Quiz prompt',
            'badge': question.hut.badge_title,
            'extra': question.hut.activity,
        }


def _rank_sources(corpus, query):
    if not query:
        return []

    query_tokens = _tokenize(query)
    ranked = []
    for source in corpus:
        score = _score_source(source['text'], query_tokens, query)
        if score:
            ranked.append((score, source))

    ranked.sort(key=lambda item: (-item[0], item[1]['title']))
    return [_format_source(source, score) for score, source in ranked[:3]]


def _score_source(text, query_tokens, query):
    if not query_tokens:
        return 0

    lowered = text.lower()
    score = 0
    for token in query_tokens:
        if token in lowered:
            score += 2

    if query.lower() in lowered:
        score += 4

    return score


def _tokenize(text):
    tokens = []
    for raw_token in text.lower().replace('-', ' ').split():
        cleaned = ''.join(character for character in raw_token if character.isalnum())
        if cleaned and cleaned not in STOP_WORDS:
            tokens.append(cleaned)
    return tokens


def _format_source(source, score):
    return {
        'title': source['title'],
        'summary': source['summary'],
        'url': source['url'],
        'source_label': source['source_label'],
        'badge': source['badge'],
        'extra': source['extra'],
        'score': score,
    }


def _default_sources():
    default_huts = Hut.objects.filter(is_active=True).order_by('display_order', 'name')[:3]
    sources = []
    for hut in default_huts:
        sources.append({
            'title': hut.name,
            'summary': hut.summary,
            'url': reverse('village:detail', kwargs={'slug': hut.slug}),
            'source_label': 'Village hut',
            'badge': hut.badge_title,
            'extra': hut.activity,
            'score': 0,
        })
    return sources


def _compose_answer(query, sources):
    if not sources:
        return 'I could not find a close match yet. Try a hut name like pottery, palmyrah, cooking, fishing, or folk music.'

    lead = sources[0]
    if not query:
        return (
            f"Start with {lead['title']}. {lead['summary']} "
            f"The hut activity is {lead['extra'].lower()}, and the badge you can earn is {lead['badge']}."
        )

    lines = [
        f"Based on the AerUla village knowledge base, {lead['title']} is the closest match for your question.",
        f"{lead['summary']}",
    ]

    if lead['source_label'] == 'Marketplace product':
        lines.append(f"It is connected to {lead['extra']} and supports a real shopping path.")
    elif lead['source_label'] == 'Simulation step':
        lines.append(f"It supports the activity path: {lead['extra']}.")
    elif lead['source_label'] == 'Quiz prompt':
        lines.append(f"You can continue by exploring the matching quiz prompt for {lead['title'].split(' quiz question')[0]}.")
    else:
        lines.append(f"The related badge is {lead['badge']} and the activity is {lead['extra'].lower()}.")

    if len(sources) > 1:
        supporting_titles = ', '.join(source['title'] for source in sources[1:])
        lines.append(f"Related sources to read next: {supporting_titles}.")

    return ' '.join(lines)


def _build_quick_prompt_links():
    guide_url = reverse('core:guide')
    links = []
    for prompt in QUICK_PROMPTS:
        links.append({
            'label': prompt,
            'url': f"{guide_url}?{urlencode({'q': prompt})}",
        })
    return links


def build_quick_prompt_links():
    return _build_quick_prompt_links()


def _generate_gemini_answer(query, sources, history):
    api_key = getattr(settings, 'GEMINI_API_KEY', '').strip()
    if not api_key:
        return None

    model = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash').strip() or 'gemini-2.0-flash'
    payload = {
        'systemInstruction': {
            'parts': [{'text': GEMINI_SYSTEM_INSTRUCTION}],
        },
        'contents': _build_gemini_contents(query, sources, history),
        'generationConfig': {
            'temperature': 0.35,
            'maxOutputTokens': 500,
        },
    }

    request = Request(
        GEMINI_API_URL.format(model=model, api_key=api_key),
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    try:
        with urlopen(request, timeout=getattr(settings, 'GEMINI_TIMEOUT_SECONDS', 20)) as response:
            raw_response = response.read().decode('utf-8')
    except (HTTPError, URLError, TimeoutError, ValueError, OSError):
        return None

    return _extract_gemini_text(raw_response)


def _build_gemini_contents(query, sources, history):
    contents = []

    for turn in history[-MAX_CHAT_TURNS:]:
        user_message = (turn.get('user') or '').strip()
        assistant_message = (turn.get('assistant') or '').strip()

        if user_message:
            contents.append({'role': 'user', 'parts': [{'text': user_message}]})

        if assistant_message:
            contents.append({'role': 'model', 'parts': [{'text': assistant_message}]})

    context_lines = [
        'Use the following AerUla context to answer the question.',
        f'Question: {query or "Give a warm AerUla introduction."}',
    ]

    if sources:
        context_lines.append('Relevant AerUla sources:')
        for source in sources:
            context_lines.append(
                f"- {source['title']} ({source['source_label']}): {source['summary']} "
                f"[badge: {source['badge']}] [action: {source['extra']}]"
            )

    contents.append(
        {
            'role': 'user',
            'parts': [{'text': '\n'.join(context_lines)}],
        }
    )

    return contents


def _extract_gemini_text(raw_response):
    try:
        payload = json.loads(raw_response)
    except json.JSONDecodeError:
        return None

    for candidate in payload.get('candidates', []):
        content = candidate.get('content', {})
        for part in content.get('parts', []):
            text = (part.get('text') or '').strip()
            if text:
                return text

    return None