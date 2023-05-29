from django.contrib import admin

from .models import (Favorite,
                     Ingredient,
                     Recipe,
                     RecipeToIngredient,
                     ShoppingCart,
                     Tag)


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(RecipeToIngredient)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
