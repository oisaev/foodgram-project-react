from django.contrib import admin

from .models import (Favorite,
                     Ingredient,
                     Recipe,
                     RecipeToIngredient,
                     ShoppingList,
                     Tag)


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(RecipeToIngredient)
admin.site.register(ShoppingList)
admin.site.register(Favorite)
