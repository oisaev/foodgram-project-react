from django.db import models


class Ingredient(models.Model):
    """Ингредиенты."""
    name = models.CharField(
        max_length=200
    )
    measurement_unit = models.CharField(
        max_length=200
    )

    def __str__(self):
        return f'{self.name} in {self.measurement_unit}'
