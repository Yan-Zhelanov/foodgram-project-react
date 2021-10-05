from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from foodgram.pagination import MyPageNumberPagination

from .filters import RecipeFilter
from .models import Recipe, Tag
from .serializers import RecipeSerializer, TagSerializer


class TagViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get',)


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'put', 'delete',)
