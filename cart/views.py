from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from cart.models import CartItem, Cart
from product.models import Product
from django.contrib import messages


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart

# get session cart global query
def get_cart(request):
    return Cart.objects.get(cart_id=_cart_id(request))

# get product global query
def get_product(product_id):
    return Product.objects.get(id=product_id)

# get cart item global query
def get_cart_item(product, cart):
    return CartItem.objects.get(product=product, cart=cart)

"""
add new cart
"""
def add_cart(request, product_id):
    product = get_product(product_id)
    try:
        cart = get_cart(request)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        # existing cart increase
        cart_item = get_cart_item(product, cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # add new fresh cart
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
        )
        cart_item.save()
    return redirect('cart-page')


"""
Decrease the cart quantity
"""
def decrease_cart(request, product_id):
    cart = get_cart(request)
    product = get_product(product_id)
    cart_items =  get_cart_item(product, cart)
    if cart_items.quantity > 1:
        cart_items.quantity -= 1
        cart_items.save()
    return redirect('cart-page')


"""
Remove the cart item
"""
def remove_cart(request, product_id):
    cart = get_cart(request)
    product = get_product(product_id)
    cart_items = get_cart_item(product, cart)
    if cart_items:
        cart_items.delete()
    messages.success(request, "Cart Remove Success")
    return redirect('cart-page')

"""
View cart page
"""
def cart_page(request, grand_total=0, tax=0, total=0, quantity=0, cart_items=None):
    try:
        cart = get_cart(request)
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


