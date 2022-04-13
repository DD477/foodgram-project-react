from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, TagViewSet, IngredientViewSet, RecipeViewSet, SubscriptionListViewSet, SubscribeViewSet, get_token

app_name = 'api'

router = routers.DefaultRouter()

router.register('users/subscriptions', SubscriptionListViewSet,
                basename='subscriptions')
router.register(r'users/(?P<author_id>[\d]+)/subscribe',
                SubscribeViewSet,
                basename='subscribe',)
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', get_token, name='get_token'),
    path('auth/', include('djoser.urls.authtoken')),
]
