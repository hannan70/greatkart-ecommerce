from django.shortcuts import render, get_object_or_404

from category.models import Category
from product.models import Product


# Create your views here.
def home_page(request):
    return render(request, "all_page/index.html")

def store_page(request):
    return render(request, "all_page/store.html")

def product_details(request, category_slug, product_slug):
    product = Product.objects.get(category__category_slug=category_slug, product_slug=product_slug)
    context = {
        "product": product
    }
    return render(request, "all_page/product-detail.html", context)