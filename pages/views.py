from django.shortcuts import render, get_object_or_404
from django.db.models import Q
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


def search(request):
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            page_products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains=keyword) | Q(product_desc__icontains=keyword))
            total_product = page_products.count()
    context = {
        'page_products': page_products,
        "total_product": total_product
    }
    return render(request, "all_page/store.html", context)