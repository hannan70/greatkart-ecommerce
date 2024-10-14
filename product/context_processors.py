from django.shortcuts import get_object_or_404
from category.models import Category
from .models import Product

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
        total_product = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-created_date')
        total_product = products.count()

    # count all cart items


    return {
        "products": products,
        'total_product': total_product
    }