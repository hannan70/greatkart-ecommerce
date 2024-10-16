from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_page, name="cart-page"),
    path("add-cart/<int:product_id>/", views.add_cart, name="add-cart"),
    path("decrease_cart/<int:product_id>/<int:cart_item_id>/", views.decrease_cart, name="decrease_cart"),
    path("remove-cart/<int:product_id>/<int:cart_item_id>/", views.remove_cart, name="remove_cart")
]