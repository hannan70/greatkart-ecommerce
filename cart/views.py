from lib2to3.fixes.fix_input import context

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from cart.models import CartItem, Cart
from product.models import Product


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1,
        )
        cart_item.save()
    return redirect('cart-page')


def cart_page(request, grand_total=0, tax=0, total=0, quantity=0, cart_items=None):

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # total and subtotal for
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)

        # tax calculate
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items': cart_items,
        'total': total,
        "grand_total": grand_total,
        "tax": tax
    }
    return render(request, "all_page/cart.html", context)


