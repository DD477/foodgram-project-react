from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe

User = get_user_model()


class IngredientSearchFilter(SearchFilter):
    """Стандартный поисковой фильтр,
    с переназначенным параметром поиска по имени ингредиента.
    """
    search_param = 'name'


class CustomFilter(FilterSet):
    """Пользовательский фильтр рецептов. Фильтрует по тегам, авторам,
    наличию рецета в списке избранного и в списке покупок.
    """
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shopping_carts__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
