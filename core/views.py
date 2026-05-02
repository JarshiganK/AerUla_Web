from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from marketplace.cart import add_product_to_session_cart
from village.models import Hut

from .services import answer_guide_question, build_ai_guide, build_chat_messages, resolve_cart_request


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
    cart_request = resolve_cart_request(query, history=history)
    if cart_request is not None:
        response = _handle_cart_request(request, cart_request)
    else:
        response = answer_guide_question(query, history=history)
    history.append({'user': query, 'assistant': response['answer'], 'sources': response['sources']})
    request.session['guide_chat_history'] = history[-6:]
    request.session.modified = True

    return JsonResponse(
        {
            'message': query,
            'answer': response['answer'],
            'sources': response['sources'],
            'actions': response.get('actions', []),
            'messages': build_chat_messages(history),
        }
    )


def _handle_cart_request(request, cart_request):
    if cart_request['status'] == 'needs_product':
        products = cart_request.get('products', [])
        return {
            'answer': cart_request['answer'],
            'sources': [_product_source(product) for product in products],
            'actions': [
                {
                    'label': f'View {product.name}',
                    'url': reverse('marketplace:detail', kwargs={'slug': product.slug}),
                }
                for product in products
            ],
            'mode': 'cart',
        }

    product = cart_request['product']
    quantity = add_product_to_session_cart(request.session, product)
    return {
        'answer': (
            f'I added {product.name} to your cart. '
            f'Your cart now has {quantity} of this item. You can review the cart or continue to checkout.'
        ),
        'sources': [_product_source(product)],
        'actions': [
            {'label': 'Go to checkout', 'url': reverse('marketplace:checkout')},
            {'label': 'View cart', 'url': reverse('marketplace:cart')},
        ],
        'mode': 'cart',
    }


def _product_source(product):
    return {
        'title': product.name,
        'summary': product.summary,
        'url': reverse('marketplace:detail', kwargs={'slug': product.slug}),
        'source_label': 'Marketplace product',
        'badge': product.status_label,
        'extra': f'{product.formatted_price} from {product.hut_name}',
    }
