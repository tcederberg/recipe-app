from django.test import TestCase
from .models import Recipe, Ingredient
from django.urls import reverse

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.
class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create Ingredients
        tea_leaves = Ingredient.objects.create(name="tea-leaves")
        water = Ingredient.objects.create(name="water")
        sugar = Ingredient.objects.create(name="sugar")

        # Create a Recipe
        image = SimpleUploadedFile(
            "../static/recipes/images/Tea.jpg", content=b"", content_type="image/jpeg"
        )
        recipe = Recipe.objects.create(
            name="Tea",
            cooking_time=5,
            description="Add tea leaves to boiling water, then add sugar",
            image=image,
        )
        recipe.ingredients.set([tea_leaves, water, sugar])

    def setUp(self):
        # Create a user and log them in before each test
        self.user = User.objects.create_user(username="test", password="decaf1234")
        self.client.login(username="test", password="decaf1234")

    def test_search_by_ingredient(self):
        response = self.client.get(reverse("search_results"), {"query": "tea-leaves"})
        self.assertContains(response, "tea")
        self.assertNotContains(response, "Coffee")

    def test_search_no_results(self):
        response = self.client.get(reverse("search_results"), {"query": "chocolate"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes found.")

    def test_description_length(self):
        recipe = Recipe.objects.get(recipe_id=1)
        desc_max_length = recipe._meta.get_field("description").max_length
        self.assertTrue(desc_max_length >= 500)

    def test_recipe_name(self):
        recipe = Recipe.objects.get(recipe_id=1)
        recipe_name_label = recipe._meta.get_field("name").verbose_name
        self.assertEqual(recipe_name_label, "name")

    def test_cooking_time_help_text(self):
        recipe = Recipe.objects.get(recipe_id=1)
        cooking_time_help_text = recipe._meta.get_field("cooking_time").help_text
        self.assertEqual(cooking_time_help_text, "in minutes")

    def test_calculate_difficulty(self):
        recipe = Recipe.objects.get(recipe_id=1)
        self.assertEqual(recipe.calculate_difficulty(), "Easy")  # Based on the given setup

    def test_ingredient_str(self):
        ingredient = Ingredient.objects.get(name="tea-leaves")
        self.assertEqual(str(ingredient), "tea-leaves")

    def test_show_all_recipes(self):
        response = self.client.get(reverse("show_all_recipes"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tea")  # Ensure the recipe 'Tea' is listed

    def test_search_by_name(self):
        response = self.client.get(
            reverse("search_results"), {"query": "Tea", "search_type": "name"}
        )
        self.assertContains(response, "Tea")
        self.assertNotContains(response, "Coffee")

    def test_search_by_cooking_time(self):
        response = self.client.get(
            reverse("search_results"), {"query": "5", "search_type": "cooking_time"}
        )
        self.assertContains(response, "Tea")

    def test_search_by_difficulty(self):
        response = self.client.get(
            reverse("search_results"), {"query": "Easy", "search_type": "difficulty"}
        )
        self.assertContains(response, "Tea")