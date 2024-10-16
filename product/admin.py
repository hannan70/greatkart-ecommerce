from django.contrib import admin
from django.utils.html import format_html
from product.models import Product, Variation


# Register your models here.
class ProductAdmin(admin.ModelAdmin):

    def thumbnail(self, object):
        return format_html("<img src='{}' width='50' style='border-radius:5px' />".format(object.product_image.url))

    list_display = ("product_name", "price", "stock", "category", "thumbnail", "created_date", "is_available")
    prepopulated_fields = {"product_slug": ("product_name", )}


class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "variation_category", "variation_value", "created_at", "is_active",)
    list_editable = ("is_active",)


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)