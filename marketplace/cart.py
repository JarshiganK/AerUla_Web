CART_SESSION_KEY = 'marketplace_cart'


def add_product_to_session_cart(session, product, quantity=1):
    cart = session.get(CART_SESSION_KEY, {})
    product_key = str(product.pk)
    cart[product_key] = cart.get(product_key, 0) + quantity
    session[CART_SESSION_KEY] = cart
    session.modified = True
    return cart[product_key]
