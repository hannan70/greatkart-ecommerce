from django.shortcuts import get_object_or_404
from category.models import Category
from .models import Product
from django.core.paginator import Paginator

def product_context_processor(request):
    category_slug = request.GET.get('category', None)
    products = None
    categories = None
    total_product = 0

    if category_slug is not None:
        # get category name by category slug
        categories = get_object_or_404(Category, category_slug=category_slug)
        # search product by category name
        products = Product.objects.filter(category=categories, is_available=True)
        # pagination
        paginator = Paginator(products, 6)
        page_number = request.GET.get("page")
        page_products = paginator.get_page(page_number)
        # count all items
        total_product = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-created_date')
        # pagination
        paginator = Paginator(products, 6)
        page_number = request.GET.get("page")
        page_products = paginator.get_page(page_number)
        # count all items
        total_product = products.count()


    return {
        "page_products": page_products,
        'total_product': total_product
    }