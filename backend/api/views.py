from django.contrib.auth import get_user_model
from django.db.models import Sum
from djoser.views import UserViewSet
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from recipes.models import (Favorite, Ingredient, Recipe, RecipeToIngredient,
                            ShoppingCart, Tag)
from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          SubscriptionListSerializer, TagSerializer)
from .utils import (add_or_del_recipe_to_favorite_or_shopping_cart,
                    download_shopping_list, subscribe_and_unsubscribe)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPageNumberPagination

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribed__user=request.user)
        page_data = self.paginate_queryset(queryset)
        serialized = SubscriptionListSerializer(
            page_data,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serialized.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id):
        return subscribe_and_unsubscribe(request, id)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для просмотра ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (IngredientFilter, )
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly, )
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        ingredients = RecipeToIngredient.objects.filter(
            recipe__shopping_cart__user=self.request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(total_amount=Sum('amount'))
        return download_shopping_list(ingredients)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        return add_or_del_recipe_to_favorite_or_shopping_cart(
            ShoppingCart, request, pk
        )

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        return add_or_del_recipe_to_favorite_or_shopping_cart(
            Favorite, request, pk
        )
