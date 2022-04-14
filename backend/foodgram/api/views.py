from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, Subscription, Tag

from .serializers import (CreateUpdateDestroyRecipeSerializer,
                          GetTokenSerializer, IngredientSerializer,
                          ListRetrieveRecipeSerializer, SubscribeSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UserSerializer, UserSetPasswordSerializer)


class ListCreateRetrieveViewSet(mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet
                                ):
    pass

User = get_user_model()

from djoser.views import UserViewSet


class UserViewSet(UserViewSet):
    queryset = User.objects.all()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ListRetrieveRecipeSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ListRetrieveRecipeSerializer
        return CreateUpdateDestroyRecipeSerializer


class ListViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet
                  ):
    pass


class SubscriptionListViewSet(ListViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return User.objects.filter(followings__user=self.request.user)


class SubscribeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SubscribeSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(
            User,
            id=self.kwargs['author_id']
        )
        serializer.save(user=self.request.user, author=author)
