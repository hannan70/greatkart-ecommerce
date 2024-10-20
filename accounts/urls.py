from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_page, name="logout")
]