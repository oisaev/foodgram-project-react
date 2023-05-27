from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet,
                    IngredientViewSet,
                    RecipeViewSet,
                    TagViewSet)

router = DefaultRouter()

router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
