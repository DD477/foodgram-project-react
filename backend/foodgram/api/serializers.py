from time import process_time

from django.contrib.auth import get_user_model
from djoser import serializers as dj_serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from recipes.models import AmountIngredientForRecipe, Ingredient, Recipe, Tag

User = get_user_model()


class UserCreateSerializer(dj_serializers.UserCreateSerializer):
    """Сериализатор для создания нового пользователя. Модель User.
    """

    class Meta:
        model = User
        fields = ('email', 'id', 'password', 'username', 'first_name',
                  'last_name',)


class UserSerializer(dj_serializers.UserSerializer):
    """Сериализатор для работы с пользователями. Модель User.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь
        на просматривакмого пользователя.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.followers.filter(user=user, author=obj.id).exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с тегами. Модель Tag.
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = '__all__',


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с ингредиентами. Модель Ingredient.
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = '__all__',


class AmountIngredientForRecipeSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для отображения количества ингредиента при
    запросе рецептов. Модель AmountIngredientForRecipe.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = AmountIngredientForRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ListRetrieveRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка рецептов, и конкретного рецепта.
    Модель Recipe.
    """
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = AmountIngredientForRecipeSerializer(
        source='amountingredientforrecipe', many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('tags', 'author', 'is_favorited',
                            'is_in_shopping_cart', 'ingredients')

    def get_is_favorited(self, obj):
        """Проверяет, находиться ли рецепт в избранном.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe_id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверяет, находиться ли рецепт в списке покупок.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.shopping_carts.filter(recipe_id=obj.id).exists()


class AmountWriteSerializer(serializers.Serializer):
    """Вспомогательный сериализатор для добавления рецептов. Для добавления
    количества конкретного ингредиента и его количества в рецепт. 
    """
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class CreateUpdateDestroyRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления, изменения, удаления рецепта.
    """
    author = UserSerializer(read_only=True)
    ingredients = AmountWriteSerializer(many=True)
    tags = serializers.ListField()
    image = Base64ImageField()
    name = serializers.CharField(max_length=200)
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time',)
        read_only_fields = ('tags', 'author', 'ingredients',)

    def to_representation(self, instance):
        return ListRetrieveRecipeSerializer(instance,
                                            context=self.context).data

    def create_amount_ingredient_for_recipe(self, recipe, ingredients):
        """Записывает ингредиенты вложенные в рецепт.
        Создает объект AmountIngredientForRecipe.
        """
        for ingredient in ingredients:
            AmountIngredientForRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
            )

    def create(self, validated_data):
        """Создает рецепт.
        """
        user = self.context['request'].user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags_data)
        self.create_amount_ingredient_for_recipe(recipe, ingredients_data)
        return recipe

    def update(self, recipe, validated_data):
        """Обновляет рецепт.
        """
        ingredients_data = validated_data.get('ingredients')
        tags = validated_data.get('tags')

        recipe.image = validated_data.get('image', recipe.image)
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time
        )

        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)

        if ingredients_data:
            recipe.amountingredientforrecipe.all().delete()
            self.create_amount_ingredient_for_recipe(recipe, ingredients_data)

        recipe.save()
        return recipe


class SimpleRecipeSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор вывода рецептов в подписках.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = '__all__',


class SubscriptionSerializer(UserSerializer):
    """Сериализатор для работы с подписками.
    """
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(*args):
        """Метод переопределен из родительского. В текущей реализации всегда
        будет возвращать True
        """
        return True

    def get_recipes(self, obj):
        """Получает рецепты для вывода их в подписках.
        Фильтрует кол-во рецептов по параметру recipes_limit.
        """
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = obj.author.recipes.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return SimpleRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """Получает кол-во рецептов автора, 
        на которого подписался пользователь.
        """
        return obj.author.recipes.count()
