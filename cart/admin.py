from django.contrib import admin

from cart.models import CartItem, Cart, Voucher

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "date_added")

class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "user", "is_active")

class VoucherAdmin(admin.ModelAdmin):
    list_display = ("voucher_name", "voucher_discount", "voucher_validity", "voucher_status")


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Voucher, VoucherAdmin)