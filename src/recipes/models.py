from django.db import models

# Create your models here.
class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    description = models.TextField()
    cooking_time = models.IntegerField()
    ingredients = models.TextField()

    def __str__(self):
        return self.name