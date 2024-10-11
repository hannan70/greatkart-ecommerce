from django.contrib import admin
from django.utils.html import format_html
from product.models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):

    def thumbnail(self, object):
        return format_html("<img src='{}' width='50' style='border-radius:5px' />".format(object.product_image.url))

    list_display = ("product_name", "price", "stock", "category", "thumbnail", "created_date", "is_available")
    prepopulated_fields = {"product_slug": ("product_name", )}


admin.site.register(Product, ProductAdmin)