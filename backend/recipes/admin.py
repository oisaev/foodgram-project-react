from django.contrib import admin

from .models import (Ingredient,
                     Tag,
                     Recipe,
                     RecipeToTag,
                     RecipeToIngredient,
                     ShopingList,
                     ShopingListToRecipe,
                     Favorites,
                     FavoriteToRecipe)


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(RecipeToTag)
admin.site.register(RecipeToIngredient)
admin.site.register(ShopingList)
admin.site.register(ShopingListToRecipe)
admin.site.register(Favorites)
admin.site.register(FavoriteToRecipe)
