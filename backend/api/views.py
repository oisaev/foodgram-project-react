from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action

from recipes.models import Ingredient, Recipe, Tag
from users.models import Subscription
from .helpers import subscribe, unsubscribe
from .serializers import (SubscriptionSerializer,
                          CustomUserSerializer,
                          IngredientSerializer,
                          RecipeReadSerializer,
                          RecipeWriteSerializer,
                          TagSerializer)

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
        if request.method == 'POST':
            return subscribe(request, id)
        return unsubscribe(request, id)


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
    queryset = Recipe.objects.all()
    
    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        pass

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, id):
        pass

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, id):
        pass
