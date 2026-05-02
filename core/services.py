import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.urls import reverse

from bookings.models import Experience
from marketplace.models import Product
from simulations.models import SimulationStep
from village.models import Hut


STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'ask', 'about', 'by', 'can', 'for', 'guide', 'how', 'is', 'me', 'of', 'or', 'the',
    'to', 'what', 'when', 'where', 'which', 'who', 'why', 'with', 'you', 'your', 'tell', 'more', 'this', 'that',
}

BOOKING_TOKENS = {
    'book', 'booking', 'reserve', 'reservation', 'experience', 'experiences', 'request', 'visit', 'workshop',
}

SHOPPING_TOKENS = {
    'add', 'buy', 'cart', 'checkout', 'order', 'purchase', 'shop',
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


def build_ai_guide(query: str | None, history=None):
    normalized_query = (query or '').strip()
    effective_query = _contextualize_query(normalized_query, history or [])
    corpus = list(_build_corpus())
    ranked_sources = _rank_sources(corpus, effective_query)

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
    guide_context = build_ai_guide(query, history=history or [])
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


def resolve_cart_request(query, history=None):
    tokens = _tokenize(query)
    if not _has_cart_intent(tokens):
        return None

    product = _resolve_product_for_cart(query, history or [])
    if product is None:
        products = _suggest_products_for_cart(query, history or [])
        return {
            'status': 'needs_product',
            'answer': (
                'I can add marketplace products to your cart. Which product should I add? '
                f"Options: {', '.join(product.name for product in products)}."
                if products
                else 'I can add marketplace products to your cart. Tell me the product name, such as Clay Serving Bowl or Handmade Water Pot.'
            ),
            'products': products,
        }

    return {
        'status': 'ready',
        'product': product,
    }


def _build_corpus():
    huts = Hut.objects.filter(is_active=True).order_by('display_order', 'name')
    experiences = Experience.objects.filter(is_published=True).select_related('hut').order_by('display_order', 'title')
    products = Product.objects.filter(is_published=True).select_related('hut').order_by('display_order', 'name')
    steps = SimulationStep.objects.select_related('hut').order_by('hut__display_order', 'correct_order')

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

    for experience in experiences:
        yield {
            'type': 'experience',
            'title': experience.title,
            'text': ' '.join([
                'book booking reserve reservation request visit workshop experience',
                experience.title,
                experience.summary,
                experience.host,
                experience.duration,
                experience.hut_name,
            ]),
            'summary': experience.summary,
            'url': reverse('bookings:request', kwargs={'slug': experience.slug}),
            'source_label': 'Bookable experience',
            'badge': experience.status_label,
            'extra': f'{experience.duration} with {experience.host} from {experience.formatted_price}',
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


def _rank_sources(corpus, query):
    if not query:
        return []

    query_tokens = _tokenize(query)
    booking_intent = _has_booking_intent(query_tokens)
    cart_intent = _has_cart_intent(query_tokens)
    ranked = []
    for source in corpus:
        score = _score_source(source, query_tokens, query, booking_intent, cart_intent)
        if score:
            ranked.append((score, source))

    ranked.sort(key=lambda item: (-item[0], item[1]['title']))
    return [_format_source(source, score) for score, source in ranked[:3]]


def _score_source(source, query_tokens, query, booking_intent=False, cart_intent=False):
    if not query_tokens:
        return 0

    text = source['text']
    lowered = text.lower()
    source_tokens = set(_tokenize(text))
    score = 0
    for token in query_tokens:
        if token in source_tokens:
            score += 2

    if query.lower() in lowered:
        score += 4

    if booking_intent:
        if source['type'] == 'experience':
            score += 8
        elif source['type'] == 'product':
            score -= 3

    if cart_intent:
        if source['type'] == 'product':
            score += 8
        elif source['type'] == 'experience':
            score -= 4

    return score


def _tokenize(text):
    tokens = []
    for raw_token in text.lower().replace('-', ' ').split():
        cleaned = ''.join(character for character in raw_token if character.isalnum())
        if cleaned and cleaned not in STOP_WORDS:
            tokens.append(cleaned)
    return tokens


def _has_booking_intent(tokens):
    return bool(set(tokens).intersection(BOOKING_TOKENS))


def _has_cart_intent(tokens):
    return bool(set(tokens).intersection(SHOPPING_TOKENS))


def _contextualize_query(query, history):
    tokens = _tokenize(query)
    if not _has_booking_intent(tokens):
        return query

    hut_context = _latest_hut_reference(history)
    if not hut_context:
        return query

    query_text = query.lower()
    if hut_context.lower() in query_text:
        return query

    return f'{query} {hut_context}'


def _resolve_product_for_cart(query, history):
    effective_query = _contextualize_product_query(query, history)
    ranked_products = _rank_products(effective_query)
    if not ranked_products:
        return None

    top_score, top_product = ranked_products[0]
    second_score = ranked_products[1][0] if len(ranked_products) > 1 else 0
    if top_score <= 0 or top_score == second_score:
        return None

    return top_product


def _suggest_products_for_cart(query, history):
    effective_query = _contextualize_product_query(query, history)
    ranked_products = _rank_products(effective_query)
    if ranked_products:
        return [product for _, product in ranked_products[:3]]

    return list(Product.objects.filter(is_published=True).select_related('hut').order_by('display_order', 'name')[:3])


def _contextualize_product_query(query, history):
    product_context = _latest_product_reference(history)
    if not product_context:
        return query

    query_text = query.lower()
    if product_context.lower() in query_text:
        return query

    return f'{query} {product_context}'


def _rank_products(query):
    tokens = _tokenize(query)
    if not tokens:
        return []

    ranked = []
    for product in Product.objects.filter(is_published=True).select_related('hut'):
        source = {
            'type': 'product',
            'text': ' '.join([product.name, product.summary, product.artisan, product.materials, product.hut_name]),
        }
        score = _score_source(source, tokens, query, cart_intent=True)
        if product.name.lower() in query.lower():
            score += 8
        if score > 0:
            ranked.append((score, product))

    ranked.sort(key=lambda item: (-item[0], item[1].display_order, item[1].name))
    return ranked


def _latest_product_reference(history):
    if not history:
        return ''

    products = list(Product.objects.filter(is_published=True).select_related('hut').order_by('display_order', 'name'))
    for turn in reversed(history[-MAX_CHAT_TURNS:]):
        text = f"{turn.get('user', '')} {turn.get('assistant', '')}".lower()
        for product in products:
            references = {
                product.slug.lower(),
                product.name.lower(),
            }
            if any(reference and reference in text for reference in references):
                return product.name

    return ''


def _latest_hut_reference(history):
    if not history:
        return ''

    huts = list(Hut.objects.filter(is_active=True).order_by('display_order', 'name'))
    for turn in reversed(history[-MAX_CHAT_TURNS:]):
        text = f"{turn.get('user', '')} {turn.get('assistant', '')}".lower()
        for hut in huts:
            references = {
                hut.slug.lower(),
                hut.short_name.lower(),
                hut.name.lower(),
                hut.name.lower().replace(' hut', ''),
            }
            if any(reference and reference in text for reference in references):
                return hut.short_name

    return ''


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
        return (
            "I couldn't find that in AerUla's curated guides yet. "
            "Ask about a hut, product, tradition, or bookable experience—"
            "for example pottery, palmyrah, cooking, fishing, folk music, or village crafts."
        )

    lead = sources[0]
    if not query:
        return (
            f"Start with {lead['title']}. {lead['summary']} "
            f"The hut activity is {lead['extra'].lower()}, and the badge you can earn is {lead['badge']}."
        )

    lines = [
        f"{lead['title']} is the closest match for your question.",
        f"{lead['summary']}",
    ]

    if lead['source_label'] == 'Marketplace product':
        lines.append(f"It is connected to {lead['extra']} and supports a real shopping path.")
    elif lead['source_label'] == 'Bookable experience':
        lines.append(
            f"I cannot submit the booking for you in chat yet, but I can point you to the request form. "
            f"This experience is {lead['extra']}."
        )
    elif lead['source_label'] == 'Simulation step':
        lines.append(f"It supports the activity path: {lead['extra']}.")
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
