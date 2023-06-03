from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeToIngredient, Tag
from users.models import Subscription
from .utils import create_ingredients

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            subscriber=request.user,
            subscribed=obj
        ).exists()


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериалайзер для неполного представления рецептов."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionSerializer(CustomUserSerializer):
    """Сериалайзер подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = CustomUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        serialized = RecipeShortSerializer(
            recipes,
            many=True
        )
        return serialized.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тега."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиента."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeToIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор связи рецепта и ингредиентов."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeToIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели рецепта для чтения."""
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        return RecipeToIngredientSerializer(
            RecipeToIngredient.objects.filter(recipe=obj),
            many=True,
        ).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.favorite.filter(user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.shopping_cart.filter(user=request.user).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели рецепта для записи."""
    ingredients = RecipeToIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.clear()
        create_ingredients(ingredients=ingredients, recipe=instance)
        instance.tags.set(tags)
        return super().update(instance, validated_data)
