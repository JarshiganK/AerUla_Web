from django.http import Http404
from django.shortcuts import render

from village.content import HUTS

from .content import PRODUCTS, get_product


def index(request):
    selected_hut = request.GET.get('hut', '')
    products = PRODUCTS

    if selected_hut:
        products = [product for product in PRODUCTS if product['hut_slug'] == selected_hut]

    context = {
        'products': products,
        'huts': HUTS,
        'selected_hut': selected_hut,
        'product_count': len(products),
    }
    return render(request, 'marketplace/index.html', context)


def detail(request, slug):
    product = get_product(slug)
    if product is None:
        raise Http404('Product not found')

    related_products = [
        item for item in PRODUCTS
        if item['hut_slug'] == product['hut_slug'] and item['slug'] != product['slug']
    ]
    return render(
        request,
        'marketplace/detail.html',
        {
            'product': product,
            'related_products': related_products,
        },
    )
