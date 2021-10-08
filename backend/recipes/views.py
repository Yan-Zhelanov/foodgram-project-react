from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from foodgram.pagination import MyPageNumberPagination
from foodgram.permissions import IsAuthorOrAdminOrReadOnly

from .filters import IngredientSearchFilter, RecipeFilter
from .models import Favorite, Ingredient, Recipe, Tag
from .serializers import (
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeShortReadSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)


class ListRetriveViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    pass


class TagViewSet(ListRetriveViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get',)


class IngredientViewSet(ListRetriveViewSet):
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter
    queryset = Ingredient.objects.all()
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

    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        saved = self.perform_update(serializer)
        serializer = RecipeReadSerializer(
            instance=saved,
            context={'request': self.request},
        )
        return Response(
            serializer.data, status=HTTP_200_OK
        )


class FavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'delete',)

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        recipe = self.get_recipe()
        try:
            Favorite.objects.create(user=request.user, recipe=recipe)
        except IntegrityError:
            return Response(
                {'errors': 'Вы уже подписаны!'},
                status=HTTP_400_BAD_REQUEST,
            )
        serializer = RecipeShortReadSerializer(recipe)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        recipe = self.get_recipe()
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
        if not favorite.exists():
            return Response(
                {'errors': 'Подписки не существует!'},
                status=HTTP_400_BAD_REQUEST,
            )
        favorite.delete()
        return Response(status=HTTP_204_NO_CONTENT)
