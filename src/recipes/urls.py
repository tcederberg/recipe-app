from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("recipes/", views.recipe_overview, name="recipe_overview"),
    path("recipes/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("search/", views.search_results, name="search_results"),
]