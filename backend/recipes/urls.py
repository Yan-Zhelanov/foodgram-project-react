from django.urls import path
from django.urls.conf import include

from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteViewSet,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet
)

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'recipes', FavoriteViewSet, basename='favorites')

app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls)),
]
