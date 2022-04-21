from django.contrib.admin import ModelAdmin, TabularInline, register
from django.utils.safestring import mark_safe

from .models import (AmountIngredientForRecipe, Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag)

EMPTY_VALUE_DISPLAY = 'Нет значения'


class IngredientInline(TabularInline):
    model = AmountIngredientForRecipe
    extra = 0


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('id', 'user', 'recipe',)

    empty_value_display = EMPTY_VALUE_DISPLAY


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'get_recipe_author',)
    list_editable = ('user', 'recipe',)

    empty_value_display = EMPTY_VALUE_DISPLAY

    def get_recipe_author(self, obj):
        return obj.recipe.author

    get_recipe_author.short_description = 'Автор рецепта'


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'get_image', 'text',
        'cooking_time', 'get_favorites_count',
    )
    readonly_fields = ('get_image',)
    filter_horizontal = ('tags',)
    list_editable = ('author', 'name', 'cooking_time',)
    fields = (
        ('name',),
        ('author',),
        ('cooking_time'),
        ('tags',),
        ('text',),
        ('image',),
    )
    search_fields = (
        'name', 'author',
    )
    list_filter = (
        'author', 'name', 'tags',
    )

    inlines = (IngredientInline,)
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    def get_favorites_count(self, obj):
        return obj.favorites.count()

    get_favorites_count.short_description = 'Число добавлений в избранное'
    get_image.short_description = 'Изображение'


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)

    empty_value_display = EMPTY_VALUE_DISPLAY


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    list_editable = ('name', 'color', 'slug',)

    empty_value_display = EMPTY_VALUE_DISPLAY
