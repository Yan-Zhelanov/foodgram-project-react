from django.urls import path

from .views import RecipeAPIView, TagAPIView

app_name = 'recipes'

urlpatterns = [
    path('recipes/', RecipeAPIView.as_view(), name='recipes'),
    path('tags/', TagAPIView.as_view(), name='tags'),
]
