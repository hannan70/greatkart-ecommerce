from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_page, name="cart-page"),
    path("add-cart/<int:product_id>/", views.add_cart, name="add-cart" )
]