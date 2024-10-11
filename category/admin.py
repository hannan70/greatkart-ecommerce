from django.contrib import admin
from django.utils.html import format_html

from category.models import Category


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html("<img src='{}' width='50' style='border-radius:5px' />".format(object.category_image.url))

    list_display = ("category_name", "category_slug", "thumbnail")
    prepopulated_fields = {"category_slug": ("category_name",)}
    list_display_links = ("category_name", "category_slug", "thumbnail")
    search_fields = ("category_name", "category_slug")
    list_filter = ("category_name",)


admin.site.register(Category, CategoryAdmin)