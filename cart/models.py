
from django.db import models

from accounts.models import Account
from product.models import Product, Variation


# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.product.product_name


    def sub_total(self):
        return self.product.price * self.quantity


class Voucher(models.Model):
    voucher_name = models.CharField(max_length=100)
    voucher_discount = models.IntegerField()
    voucher_validity = models.DateField()
    voucher_status = models.BooleanField(default=True)

    def __str__(self):
        return self.voucher_name












