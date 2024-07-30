from django.shortcuts import render
from .models import Recipe, Ingredient
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "recipes/recipes_home.html")


@login_required
def recipe_overview(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes/recipe_overview.html", {"recipes": recipes})


@login_required
def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    difficulty = recipe.calculate_difficulty()
    return render(
        request, "recipes/recipe_detail.html", {"recipe": recipe, "difficulty": difficulty}
    )


@login_required
def search_by_ingredient(request):
    query = request.GET.get("query")
    if query:
        recipes = Recipe.objects.filter(ingredients__name__icontains=query).distinct()
    else:
        recipes = Recipe.objects.none()
    return render(request, "recipes/search_results.html", {"recipes": recipes})


@login_required
def search_results(request):
    query = request.GET.get("query")
    recipes = Recipe.objects.filter(ingredients__name__icontains=query)
    if not recipes:
        return render(request, "recipes/search_results.html", {"message": "No recipes found."})
    return render(request, "recipes/search_results.html", {"recipes": recipes})