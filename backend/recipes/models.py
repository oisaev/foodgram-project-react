from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


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
        ordering = ('name',)

    def __str__(self):
        return self.name


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
        verbose_name_plural = 'ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return f'{self.name} в {self.measurement_unit}'


class Recipe(models.Model):
    """Модель рецептов."""
    tags = models.ManyToManyField(
        Tag,
        verbose_name='теги рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
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
    published = models.DateTimeField(
        verbose_name='дата и время публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-published',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'name'),
                name='unique_author_name'
            )
        ]

    def __str__(self):
        return self.name


class RecipeToIngredient(models.Model):
    """Модель связь рецепта и ингредиентов."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_to_ingredient',
        verbose_name='ссылка на рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_to_ingredient',
        verbose_name='ссылка на ингредиент'
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Количество не может быть меньше 1'
            )
        ],
        verbose_name='количество ингредиента в рецепте'
    )

    class Meta:
        verbose_name = 'связь рецепта и ингредиентов'
        verbose_name_plural = 'связи рецепта и ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return (
            f'{self.ingredient.name}'
            f' {self.amount} {self.ingredient.measurement_unit}'
            f' в рецепте {self.recipe.name}'
        )


class ShoppingCart(models.Model):
    """Модель списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='рецепт для покупки'
    )

    class Meta:
        verbose_name = 'рецепт для покупок'
        verbose_name_plural = 'рецепты для покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe_in_shopping_list'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'


class Favorite(models.Model):
    """Модель избранных рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='избранный рецепт'
    )

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe_in_favorites'
            )
        ]

    def __str__(self):
        return f'{self.recipe} любимый у {self.user}'
