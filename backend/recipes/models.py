from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


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


class Tag(models.Model):
    """Тэги."""
    name = models.CharField(
        max_length=200
    )
    color = models.CharField(
        max_length=7,
        null=True,
        blank=True
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг тэга'
    )


class Recipe(models.Model):
    """Рецепты."""
    tags = models.ManyToManyField(
        Tag,
        through='RecipeToTag'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeToIngredient'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Фотография блюда'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления должно быть не менее 1 минуты'
            )
        ],
        verbose_name='Время приготовления (в минутах)'
    )


class RecipeToTag(models.Model):
    """Связь рецепта и тэгов."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на тэг'
    )


class RecipeToIngredient(models.Model):
    """Связь рецепта и ингредиентов."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на ингредиент'
    )


class Purchases(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Покупатель'
    )
    reсipes = models.ManyToManyField(
        Recipe,
        through='PurchaseToRecipes',
        verbose_name='Покупки'
    )


class PurchaseToRecipes(models.Model):
    purchase = models.ForeignKey(
        Purchases,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на покупку'
    )
    reсipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на рецепт'
    )


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    favorites = models.ManyToManyField(
        Recipe,
        through='FavoriteToRecipes',
        verbose_name='Покупки'
    )


class FavoriteToRecipes(models.Model):
    favorite = models.ForeignKey(
        Favorites,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на покупку'
    )
    reсipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на рецепт'
    )
