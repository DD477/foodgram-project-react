from rest_framework import serializers

from recipes.models import Subscription, Tag, Ingredient, Recipe, AmountIngredientForRecipe
from users.models import User

import base64

from django.core.files.base import ContentFile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password', 'is_subscribed')

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        user = self.context['request'].user
        author = obj
        query = Subscription.objects.filter(user=author, author=user)
        if query:
            return True
        return False

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            del self.fields['is_subscribed']
        return data


class UserSetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        required=True
    )
    current_password = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ('new_password', 'current_password')


class GetTokenSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True
    )
    email = serializers.CharField(
        required=True
    )


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngredientForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = AmountIngredientForRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


# class Base64ImageField(serializers.ImageField):
#     def from_native(self, data):
#         if isinstance(data, basestring) and data.startswith('data:image'):
#             # base64 encoded image - decode
#             format, imgstr = data.split(';base64,')  # format ~= data:image/X,
#             ext = format.split('/')[-1]  # guess file extension

#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

#         return super(Base64ImageField, self).from_native(data)


# class Base64ImageField(serializers.Field):
#     def to_representation(self, value):
#         return value

#     def to_internal_value(self, data):
#         try:
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

#             print('===========')
#             print('format = ', format)
#             print('imgstr = ', imgstr)
#             print('ext = ', ext)
#             print('data = ', data)
#             print('===========')

#         except ValueError:
#             raise serializers.ValidationError('Ошибка!!!')
#         return data


class RecipeListRetriveSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    ingredient = AmountIngredientForRecipeSerializer(
        source="amountingredientforrecipe", many=True)
    # image = Base64ImageField()

    class Meta:
        model = Recipe
        depth = 1
        fields = '__all__'

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False

class RecipewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
