from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=200,
        verbose_name='название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='единица измерения ингредиента'
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'нигредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return f'{self.name} в {self.measurement_unit}'


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='название тега'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='цвет тега'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='slug тега'
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    tags = models.ManyToManyField(
        Tag,
        through='RecipeToTag',
        verbose_name='теги рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeToIngredient',
        verbose_name='ингредиенты рецепта'
    )
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='название рецепта'
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='фотография блюда'
    )
    text = models.TextField(
        verbose_name='описание рецепта'
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления должно быть не менее 1 минуты'
            )
        ],
        verbose_name='время приготовления (в минутах)'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class RecipeToTag(models.Model):
    """Модель связи рецепта и тегов."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='ссылка на рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='ссылка на тег'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_recipe_tag'
            )
        ]


class RecipeToIngredient(models.Model):
    """Модель связь рецепта и ингредиентов."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='ссылка на рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ссылка на ингредиент'
    )
    quantity = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Количество не может быть меньше 1'
            )
        ],
        verbose_name='количество ингредиента в рецепте'
    )


class ShopingList(models.Model):
    """Модель листа покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='покупатель'
    )
    reсipes = models.ManyToManyField(
        Recipe,
        through='ShopingListToRecipe',
        verbose_name='покупки'
    )


class ShopingListToRecipe(models.Model):
    """Модель связи листа покупок и рецептов."""
    purchase = models.ForeignKey(
        ShopingList,
        on_delete=models.CASCADE,
        verbose_name='ссылка на покупку'
    )
    reсipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='ссылка на рецепт'
    )


class Favorites(models.Model):
    """Модель избранных рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    favorites = models.ManyToManyField(
        Recipe,
        through='FavoriteToRecipe',
        verbose_name='покупки'
    )


class FavoriteToRecipe(models.Model):
    """Модель связи избранных рецептов с рецептами."""
    favorite = models.ForeignKey(
        Favorites,
        on_delete=models.CASCADE,
        verbose_name='ссылка на покупку'
    )
    reсipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='ссылка на рецепт'
    )
