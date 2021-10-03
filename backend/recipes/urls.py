from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')

app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls)),
]
