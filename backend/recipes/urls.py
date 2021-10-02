from backend.recipes.views import RecipesAPIView
from django.urls import path

app_name = 'recipes'

urlpatterns = [
    path('recipes/', RecipesAPIView.as_view(), name='recipes'),
]
