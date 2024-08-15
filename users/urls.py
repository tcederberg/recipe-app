from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),  # URL pattern for logging out
    path("logout-success/", views.logout_success, name="logout_success"),
]