from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, TagAPIView

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')

app_name = 'recipes'

urlpatterns = [
    path('tags/', TagAPIView.as_view(), name='tags'),
    path('', include(router.urls)),
]
