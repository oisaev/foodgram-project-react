from django.contrib import admin

from .models import (Favorite,
                     Ingredient,
                     Recipe,
                     RecipeToIngredient,
                     ShoppingCart,
                     Tag)


class IngredientInline(admin.TabularInline):
    model = RecipeToIngredient


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientInline,
    ]
    list_display = ('id', 'name', 'author', 'favorites_count')
    list_filter = ('author', 'name', 'tags')

    def favorites_count(self, obj):
        return obj.favorite.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeToIngredient)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
