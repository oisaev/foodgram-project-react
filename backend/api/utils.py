from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe, RecipeToIngredient
from users.models import Subscription
from .serializers import SubscriptionSerializer

User = get_user_model()


def subscribe_and_unsubscribe(request, subscribed_id):
    """Функция подписки и отписки на/от автора рецептов."""
    subscribed = get_object_or_404(User, id=subscribed_id)
    instance = Subscription.objects.filter(
        subscriber=request.user,
        subscribed=subscribed
    )
    if request.method == 'POST' and not instance.exists():
        subscription = Subscription.objects.create(
            subscriber=request.user,
            subscribed=subscribed
        )
        serialized = SubscriptionSerializer(subscription)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE' and instance.exists():
        Subscription.objects.filter(
            subscriber=request.user,
            subscribed=subscribed
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def create_ingredients(ingredients, recipe):
    """Функция для добавления ингредиентов в рецепт."""
    for ingredient in ingredients:
        RecipeToIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=ingredient['id'],
            amount=ingredient['amount']
        )


def download_shopping_list(ingredients):
    """Функция скачивания списка ингредиентов для покупки."""
    file_name = 'shopping_list.txt'
    file_content = 'Следующие продукты нужно купить:\n\n'
    for ingredient in ingredients:
        file_content += (
            f'{ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]}) - '
            f'{ingredient["amount"]}\n'
        )
    response = HttpResponse(file_content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response


def add_or_del_recipe_to_favorite_or_shopping_cart(
        model, request, recepe_id
):
    """Функция добавления и удаление рецепта
    в/из избранное или список покупок."""
    recipe = get_object_or_404(Recipe, id=recepe_id)
    instance = model.objects.filter(
        user=request.user,
        recipe=recipe
    )
    if request.method == 'POST' and not instance.exists():
        model.objects.create(
            recipe=recipe,
            user=request.user
        )
        serializer = Recipe(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE' and instance.exists():
        model.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
