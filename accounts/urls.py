from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('register', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forget-password/", views.forget_password, name="forget-password"),
    path("reset-password-validate/<uidb64>/<token>/", views.reset_password_validate, name="reset-password-validate"),
    path("reset-password/", views.reset_password, name="reset-password"),
]