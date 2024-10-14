from cart.models import CartItem, Cart
from cart.views import get_cart


def cart_content_processor(request):
    cart_count = 0
    if "admin" in request.path:
        return  {}
    else:
        try:
            cart = get_cart(request)
            cart_items = CartItem.objects.all().filter(cart=cart)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0

    return {
        'cart_count' : cart_count
    }