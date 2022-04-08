from django.contrib import admin

from .models import Recipe, ShoppingCart, Favorite, Subscription, Ingredient, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'text',
        'author',
        'get_tags',
        'image',
        'cooking_time',
        'get_ingredients',
    )

    filter_horizontal = ('tags', 'ingredients',)

    def get_tags(self, obj):
        return ", ".join([str(t)] for t in obj.tags.all())

    def get_ingredients(self, obj):
        return ", ".join([str(i)] for i in obj.ingredients.all())


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
    )
    filter_horizontal = ('recipe',)


@admin.register(Favorite)
class FavoriteCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
    )
    filter_horizontal = ('recipe',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
