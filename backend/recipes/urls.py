from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteAPIView,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
)

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

app_name = 'recipes'

urlpatterns = [
    path(
        'recipes/<int:id>/favorite/',
        FavoriteAPIView.as_view(),
        name='favorite',
    ),
    path('', include(router.urls)),
]
