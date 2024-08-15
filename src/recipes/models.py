from django.db import models
from django.shortcuts import reverse



class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=500)
    cooking_time = models.FloatField(
        help_text="in minutes"
    )  # Using FloatField for precision
    ingredients = models.ManyToManyField(Ingredient)
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    

    def calculate_difficulty(self):
        ingredient_count = self.ingredients.count()
        if self.cooking_time < 10 and ingredient_count < 4:
            return "Easy"
        elif self.cooking_time < 10 and ingredient_count >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and ingredient_count < 4:
            return "Intermediate"
        else:
            return "Hard"

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name