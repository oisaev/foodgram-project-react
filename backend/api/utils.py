from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from users.models import Subscription
from .serializers import RecipeShortSerializer, SubscriptionListSerializer

User = get_user_model()


def subscribe_and_unsubscribe(request, author_id):
    """Функция подписки и отписки на/от автора рецептов."""
    user = request.user
    author = get_object_or_404(User, id=author_id)
    instance_exists = Subscription.objects.filter(
        user=user,
        author=author
    ).exists()
    if request.method == 'POST' and not instance_exists:
        serializer = SubscriptionListSerializer(
            author,
            context={'request': request}
        )
        Subscription.objects.create(user=user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE' and instance_exists:
        Subscription.objects.filter(
            user=request.user,
            author=author
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def download_shopping_list(ingredients):
    """Функция скачивания списка ингредиентов для покупки."""
    file_name = 'shopping_list.txt'
    file_content = 'Следующие продукты нужно купить:\n\n'
    for ingredient in ingredients:
        file_content += (
            f'{ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]}) - '
            f'{ingredient["total_amount"]}\n'
        )
    response = HttpResponse(file_content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response


def add_or_del_recipe_to_favorite_or_shopping_cart(
        model, request, recepe_id
):
    """Функция добавления и удаление рецепта
    в/из избранное или список покупок."""
    recipe = get_object_or_404(Recipe, pk=recepe_id)
    instance_exists = model.objects.filter(
        user=request.user,
        recipe=recipe
    ).exists()
    if request.method == 'POST' and not instance_exists:
        model.objects.create(
            recipe=recipe,
            user=request.user
        )
        serialized = RecipeShortSerializer(recipe)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE' and instance_exists:
        model.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
