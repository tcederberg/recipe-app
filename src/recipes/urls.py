from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # Update the URL name to 'recipe_overview' if you want to keep using that in your template.
    path("recipes/overview/", views.combined_charts_overview, name="recipe_overview"),
    # If you want a separate URL for just the combined charts, you can keep this.
    path("recipes/combined-charts/", views.combined_charts_overview, name="combined_charts_overview"),
    path("recipes/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("search/", views.search_results, name="search_results"),
    path("all_recipes/", views.show_all_recipes, name="show_all_recipes"),
]