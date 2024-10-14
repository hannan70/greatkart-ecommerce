from django.shortcuts import render, get_object_or_404

from cart.models import CartItem
from cart.views import _cart_id, get_cart
from product.models import Product


# Create your views here.
def home_page(request):
    return render(request, "all_page/index.html")

def store_page(request):
    return render(request, "all_page/store.html")

def product_details(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__category_slug=category_slug, product_slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        "single_product": single_product,
        'in_cart': in_cart
    }
    return render(request, "all_page/product-detail.html", context)