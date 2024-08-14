from django.shortcuts import render
from .models import Recipe, Ingredient
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.urls import reverse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from io import BytesIO
import base64
from django.db.models.functions import TruncMonth
from django_pandas.io import read_frame


@login_required
def home(request):
    return render(request, "recipes/recipes_home.html")


@login_required
def recipe_overview(request):
    recipes = Recipe.objects.all()
    graphic = generate_difficulty_graphic(recipes)

    difficulty_urls = {
        "Easy": reverse("search_results") + "?search_type=difficulty&query=Easy",
        "Medium": reverse("search_results") + "?search_type=difficulty&query=Medium",
        "Intermediate": reverse("search_results")
        + "?search_type=difficulty&query=Intermediate",
        "Hard": reverse("search_results") + "?search_type=difficulty&query=Hard",
    }

    return render(
        request,
        "app/recipe_overview.html",
        {"graphic": graphic, "difficulty_urls": difficulty_urls},
    )


def generate_difficulty_graphic(recipes):
    difficulty_counts = {"Easy": 0, "Medium": 0, "Intermediate": 0, "Hard": 0}
    for recipe in recipes:
        difficulty = recipe.calculate_difficulty()
        difficulty_counts[difficulty] += 1

    fig, ax = plt.subplots()
    ax.bar(difficulty_counts.keys(), difficulty_counts.values())
    ax.set_xlabel("Difficulty Level")
    ax.set_ylabel("Number of Recipes")
    ax.set_title("Recipe Difficulty Distribution")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    return base64.b64encode(image_png).decode("utf-8")


def generate_ingredient_pie_chart_graphic():
    recipes = Recipe.objects.all()
    ingredient_counts = [recipe.ingredients.count() for recipe in recipes]
    count_ranges = ["1-3", "4-6", "7-9", ">9"]
    count_categories = {range_: 0 for range_ in count_ranges}

    for count in ingredient_counts:
        if count <= 3:
            count_categories["1-3"] += 1
        elif count <= 6:
            count_categories["4-6"] += 1
        elif count <= 9:
            count_categories["7-9"] += 1
        else:
            count_categories[">9"] += 1

    fig, ax = plt.subplots()
    ax.pie(count_categories.values(), labels=count_categories.keys(), autopct="%1.1f%%")
    ax.set_title("Recipe Distribution by Number of Ingredients")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    return base64.b64encode(image_png).decode("utf-8")


def generate_cooking_time_trend_graphic():
    # Fetch the recipes and their cooking times
    recipes = Recipe.objects.all().order_by('name')
    recipe_names = [recipe.name for recipe in recipes]
    cooking_times = [recipe.cooking_time for recipe in recipes]

    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size as needed
    ax.scatter(recipe_names, cooking_times, marker='o')

    # Set the labels and title
    ax.set_xlabel("Recipe Name")
    ax.set_ylabel("Cooking Time (minutes)")
    ax.set_title("Cooking Time per Recipe")

    # Set the y-axis limits and tick intervals
    ax.set_ylim(0, 30)
    ax.yaxis.set_ticks(range(0, 31, 5))

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Ensure everything fits without overlapping
    plt.tight_layout()

    # Save the plot to a PNG buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image to base64
    return base64.b64encode(image_png).decode('utf-8')


@login_required
def combined_charts_overview(request):
    recipes = Recipe.objects.all()
    difficulty_graphic = generate_difficulty_graphic(recipes)
    ingredient_pie_chart_graphic = generate_ingredient_pie_chart_graphic()
    cooking_time_trend_graphic = generate_cooking_time_trend_graphic()

    difficulty_urls = {
        "Easy": reverse("search_results") + "?search_type=difficulty&query=Easy",
        "Medium": reverse("search_results") + "?search_type=difficulty&query=Medium",
        "Intermediate": reverse("search_results") + "?search_type=difficulty&query=Intermediate",
        "Hard": reverse("search_results") + "?search_type=difficulty&query=Hard",
    }

    return render(
        request,
        "recipes/recipe_overview.html",
        {
            "recipes": recipes,
            "difficulty_graphic": difficulty_graphic,
            "ingredient_pie_chart_graphic": ingredient_pie_chart_graphic,
            "cooking_time_trend_graphic": cooking_time_trend_graphic,
            "difficulty_urls": difficulty_urls,
        },
    )


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
def show_all_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes/all_recipes.html", {"recipes": recipes})


@login_required
def search_results(request):
    query = request.GET.get("query", "")
    search_type = request.GET.get("search_type", "name")

    if query:
        if search_type == "name":
            recipes = Recipe.objects.filter(name__icontains=query)
        elif search_type == "ingredient":
            ingredients = Ingredient.objects.filter(name__icontains=query)
            recipes = Recipe.objects.filter(ingredients__in=ingredients).distinct()
        elif search_type == "cooking_time":
            try:
                time_query = float(query)
                recipes = Recipe.objects.filter(cooking_time__lte=time_query)
            except ValueError:
                recipes = Recipe.objects.none()  # Handles non-numeric input
        elif search_type == "difficulty":
            all_recipes = Recipe.objects.all()
            recipes = [
                recipe
                for recipe in all_recipes
                if recipe.calculate_difficulty() == query.capitalize()
            ]
        else:
            recipes = Recipe.objects.none()
    else:
        recipes = Recipe.objects.none()

    if isinstance(recipes, list):
        recipes_qs = Recipe.objects.filter(pk__in=[r.pk for r in recipes])
        recipes_df = read_frame(recipes_qs)
    else:
        recipes_df = read_frame(recipes)

    return render(
        request,
        "recipes/search_results.html",
        {"recipes": recipes, "query": query, "search_type": search_type},
    )