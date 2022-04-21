from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser import views as dj_views
from rest_framework import status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import (AmountIngredientForRecipe, Favorite, Ingredient,
                            Recipe, ShoppingCart, Tag)
from .filters import CustomFilter, IngredientSearchFilter
from .paginators import PageLimitPagination
from .permissions import IsAuthorIsStaffOrReadOnly
from .serializers import (CreateUpdateDestroyRecipeSerializer,
                          IngredientSerializer, ListRetrieveRecipeSerializer,
                          SimpleRecipeSerializer, SubscriptionSerializer,
                          TagSerializer)

User = get_user_model()


class UserViewSet(dj_views.UserViewSet):
    queryset = User.objects.all()
    pagination_class = PageLimitPagination

    @action(detail=True, methods=('post',), url_path='subscribe',
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response(
                {'errors': 'Вы не можете подписываться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.subscribe.filter(id=author.id).exists():
            return Response(
                {'errors': 'Вы уже подписаны на данного пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.subscribe.add(author)
        serializer = SubscriptionSerializer(
            author, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {'errors': 'Вы не можете отписываться от самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if author:
            user.subscribe.remove(author)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Вы уже отписались'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=('get',), url_path='subscriptions',
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = user.subscribe.all()
        pagination = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pagination,
            data=list(request.data),
            many=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


@permission_classes([IsAuthorIsStaffOrReadOnly])
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = CustomFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ListRetrieveRecipeSerializer
        return CreateUpdateDestroyRecipeSerializer

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Favorite, request.user, pk)
        return None

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(ShoppingCart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(ShoppingCart, request.user, pk)
        return None

    @action(detail=False, methods=('get',),
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = self.request.user
        if not user.shopping_carts.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = AmountIngredientForRecipe.objects.filter(
            recipe__in=(user.shopping_carts.values('recipe_id'))
        ).values(
            ingredients=F('ingredient__name'),
            measure=F('ingredient__measurement_unit')
        ).annotate(amount_sum=Sum('amount'))

        filename = f'{user.username}_shopping_list.txt'
        shopping_list = ''
        for ing in ingredients:
            shopping_list += (
                f'{ing["ingredients"]}: {ing["amount_sum"]} {ing["measure"]}\n'
            )

        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    def add_obj(self, model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        _, created = model.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            return Response({
                'errors': 'Рецепт уже добавлен в список'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = SimpleRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, id):
        obj = model.objects.filter(user=user, recipe__id=id)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)
