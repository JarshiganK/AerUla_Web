from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string

from village.models import Hut

from .cart import CART_SESSION_KEY, add_product_to_session_cart
from .forms import CheckoutForm
from .models import Product
from .models import Order, OrderItem


def index(request):
    selected_hut = request.GET.get('hut', '')
    products = Product.objects.filter(is_published=True).select_related('hut')

    if selected_hut:
        products = products.filter(hut__slug=selected_hut)

    context = {
        'products': products,
        'huts': Hut.objects.filter(is_active=True),
        'selected_hut': selected_hut,
        'product_count': products.count(),
    }
    return render(request, 'marketplace/index.html', context)


def detail(request, slug):
    try:
        product = Product.objects.select_related('hut').get(slug=slug, is_published=True)
    except Product.DoesNotExist:
        raise Http404('Product not found')

    related_products = Product.objects.filter(
        hut=product.hut,
        is_published=True,
    ).exclude(pk=product.pk)[:3]
    return render(
        request,
        'marketplace/detail.html',
        {
                'product': product,
                'related_products': related_products,
        },
    )


def add_to_cart(request, slug):
    try:
        product = Product.objects.get(slug=slug, is_published=True)
    except Product.DoesNotExist:
        raise Http404('Product not found')

    add_product_to_session_cart(request.session, product)
    return redirect('marketplace:cart')


def cart(request):
    cart_items, cart_total = _cart_items(request)
    return render(
        request,
        'marketplace/cart.html',
        {
            'cart_items': cart_items,
            'cart_count': len(cart_items),
            'cart_total': f'LKR {cart_total:,.0f}',
        },
    )


def checkout(request):
    cart_items, cart_total = _cart_items(request)
    if not cart_items:
        return redirect('marketplace:cart')

    order = None
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                reference=_new_order_reference(),
                customer_name=form.cleaned_data['customer_name'],
                customer_email=form.cleaned_data['customer_email'],
                total=cart_total,
                status=Order.STATUS_PLACED,
            )
            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    unit_price=item['product'].price,
                )
                for item in cart_items
            ])
            request.session[CART_SESSION_KEY] = {}
            request.session.modified = True
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'customer_name': request.user.get_full_name() or request.user.username,
                'customer_email': request.user.email,
            }
        form = CheckoutForm(initial=initial)

    return render(
        request,
        'marketplace/checkout.html',
        {
            'form': form,
            'order': order,
            'cart_items': cart_items,
            'cart_total': f'LKR {cart_total:,.0f}',
        },
    )


def _cart_items(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    products = Product.objects.filter(pk__in=cart.keys(), is_published=True).select_related('hut')
    product_map = {str(product.pk): product for product in products}
    items = []
    total = 0
    for product_id, quantity in cart.items():
        product = product_map.get(str(product_id))
        if product is None:
            continue
        line_total = product.price * quantity
        total += line_total
        items.append({
            'product': product,
            'quantity': quantity,
            'line_total': f'LKR {line_total:,.0f}',
        })
    return items, total


def _new_order_reference():
    return f'AER-{get_random_string(8).upper()}'
