from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from cart.models import CartItem, Cart, Voucher
from product.models import Product, Variation
from django.contrib import messages
from datetime import date


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
    if request.user.is_authenticated and request.user.is_active:
        product = get_product(product_id)
        product_variation = []
        # add variation
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    # check same product and same variation. it's okay or not
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        # add cart session id
        try:
            cart = get_cart(request)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        exists_cart = CartItem.objects.filter(product=product, cart=cart, user=request.user).exists()

        if exists_cart:
            # existing cart increase
            cart_item = CartItem.objects.filter(product=product, cart=cart, user=request.user)
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in existing_variation_list:
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, cart=cart, user=request.user, quantity=1)
                if len(product_variation) > 0:
                    item.variation.clear()
                    for i in product_variation:
                        item.variation.add(i)

                item.save()

        else:
            # add new fresh cart
            item = CartItem.objects.create(product=product, cart=cart, user=request.user, quantity=1)
            if len(product_variation) > 0:
                item.variation.clear()
                for i in product_variation:
                    item.variation.add(i)
            item.save()
        return redirect('cart-page')
    else:
        messages.error(request, "Please login first")
        return redirect(request.META.get('HTTP_REFERER', '/'))


"""
Decrease the cart quantity
"""
def decrease_cart(request, product_id, cart_item_id):
    cart = get_cart(request)
    product = get_product(product_id)

    try:
        cart_items = CartItem.objects.get(product=product, cart=cart, id=cart_item_id, user=request.user)
        if cart_items.quantity > 1:
            cart_items.quantity -= 1
            cart_items.save()
    except:
        pass
    return redirect('cart-page')


"""
Remove the cart item
"""
def remove_cart(request, product_id, cart_item_id):
    cart = get_cart(request)
    product = get_product(product_id)
    try:
        cart_items = CartItem.objects.get(product=product, cart=cart, id=cart_item_id, user=request.user)
        if cart_items:
            cart_items.delete()
        messages.success(request, "Cart Remove Success")
    except:
        messages.error(request, "Cart Remove Failed")
    return redirect('cart-page')

"""
View cart page
"""
@login_required(login_url='login')
def cart_page(request, grand_total=0, tax=0, total=0, quantity=0, cart_items=None):

    # get all active cart
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)

    # total and subtotal for
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
    # tax calculate
    tax = (2*total)/100
    grand_total = total + tax

    context = {
        'cart_items': cart_items,
        'total': total,
        "grand_total": grand_total,
        "tax": tax
    }
    return render(request, "all_page/cart.html", context)


def voucher(request):
    if request.method == 'POST':
        voucher_name = request.POST.get("voucher_name")
        voucher = Voucher.objects.filter(voucher_name__exact=voucher_name).filter(voucher_validity__gte=date.today()).filter(voucher_status=True).exists()

        if voucher:
            voucher_discount = Voucher.objects.filter(voucher_name__exact=voucher_name).values("voucher_discount").first()
            discount_percentage = voucher_discount['voucher_discount']
            grand_total = request.POST.get("grand_total")
            original_price = float(grand_total)

            discount_amount = original_price * (discount_percentage / 100)
            discounted_price = original_price - discount_amount
            request.session['discounted_price'] = discounted_price


    return JsonResponse({"success": "Voucher Applied", "grand_total": discounted_price })


def checkout_page(request, grand_total=0, tax=0, total=0, quantity=0, cart_items=None):
    return

