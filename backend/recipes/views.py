from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from foodgram.pagination import MyPageNumberPagination
from foodgram.permissions import IsAuthorOrAdminOrReadOnly

from .filters import RecipeFilter
from .models import Recipe, Tag
from .serializers import (
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)


class TagViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get',)


class RecipeViewSet(ModelViewSet):
    pagination_class = MyPageNumberPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'put', 'delete',)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved = self.perform_create(serializer)
        serializer = RecipeReadSerializer(
            instance=saved,
            context={'request': self.request}
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=HTTP_201_CREATED, headers=headers
        )
