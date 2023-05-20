from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet,
                    TagViewSet,
                    RecipeViewSet,
                    UserViewSet)

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
