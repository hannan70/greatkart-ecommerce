from django.urls import path
from .import views

urlpatterns = [
    path("", views.home_page, name="home-page"),
    path("store/", views.store_page, name="store-page"),
    path("store/<slug:category_slug>/<slug:product_slug>/", views.product_details, name="product-details")

]