from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Recipe
from .serializers import RecipeSerializer


class TagAPIView(GenericAPIView):
    pass


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'put', 'delete',)
