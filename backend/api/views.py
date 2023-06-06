from django.db.models import Sum
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action

from recipes.models import (Favorite,
                            Ingredient,
                            Recipe,
                            RecipeToIngredient,
                            ShoppingCart,
                            Tag)
from users.models import Subscription
from .filters import RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer,
                          IngredientSerializer,
                          RecipeReadSerializer,
                          RecipeWriteSerializer,
                          SubscriptionSerializer,
                          TagSerializer)
from .utils import (add_or_del_recipe_to_favorite_or_shopping_cart,
                    download_shopping_list,
                    subscribe_and_unsubscribe)


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        queryset = Subscription.objects.filter(user=request.user)
        datapage = self.paginate_queryset(queryset)
        serialized_data = SubscriptionSerializer(datapage, many=True)
        return self.get_paginated_response(self, serialized_data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id):
        return subscribe_and_unsubscribe(request, id)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для просмотра ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly, )
    filterset_class = RecipeFilter

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
        ).annotate(amount=Sum('amount'))
        return download_shopping_list(ingredients)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, id):
        return add_or_del_recipe_to_favorite_or_shopping_cart(
            ShoppingCart, request, id
        )

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, id):
        return add_or_del_recipe_to_favorite_or_shopping_cart(
            Favorite, request, id
        )
