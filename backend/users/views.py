from django.db import IntegrityError
from django.http import Http404, FileResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.viewsets import GenericViewSet

from foodgram.settings import MEDIA_ROOT
from foodgram.pagination import LimitPageNumberPagination
from recipes.serializers import RecipeShortReadSerializer

from .models import ShoppingCart, Subscribe, User
from .serializers import SubscriptionSerializer

MEASUREMENT_UNIT = 0
AMOUNT = 1

FILE_NAME = 'shopping_cart.txt'


class UserSubscribeViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination
    lookup_url_kwarg = 'user_id'

    def get_subscribtion_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return SubscriptionSerializer(*args, **kwargs)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        self.get_serializer
        queryset = [
            subscribe.author for subscribe in request.user.subscriber.all()
        ]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_subscribtion_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_subscribtion_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create_subscribe(self, request, author):
        if request.user == author:
            return Response(
                {'errors': 'Нельзя подписаться на самого себя!'},
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            subscribe = Subscribe.objects.create(
                user=request.user,
                author=author,
            )
        except IntegrityError:
            return Response(
                {'errors': 'Нельзя подписаться дважды!'},
                status=HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_subscribtion_serializer(subscribe.author)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete_subscribe(self, request, author):
        try:
            Subscribe.objects.get(user=request.user, author=author).delete()
        except Subscribe.DoesNotExist:
            return Response({
                    'errors': (
                        'Нельзя отписаться от данного пользователя,'
                        ' если вы не подписаны на него!'
                    )
                },
                status=HTTP_400_BAD_REQUEST,
            )
        return Response(
            status=HTTP_204_NO_CONTENT
        )

    @action(
        methods=('get', 'delete',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, user_id=None):
        try:
            author = get_object_or_404(User, pk=user_id)
        except Http404:
            return Response(
                {'detail': 'Пользователь не найден!'},
                status=HTTP_404_NOT_FOUND,
            )
        if request.method == 'GET':
            return self.create_subscribe(request, author)
        return self.delete_subscribe(request, author)


class ShoppingCartViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeShortReadSerializer
    queryset = ShoppingCart.objects.all()
    http_method_names = ('get', 'delete',)

    def generate_shopping_cart_data(self, request):
        recipes = (
            request.user.shopping_cart.recipes.prefetch_related('ingredients')
        )
        ingredients = {}
        for recipe in recipes:
            for ingredient in recipe.ingredients.all():
                if ingredient.pk not in ingredients:
                    ingredients[ingredient.ingredient.name] = [
                        ingredient.ingredient.measurement_unit,
                        ingredient.amount
                    ]
                    continue
                ingredients[ingredient.name][AMOUNT] += ingredient.amount
        return ingredients

    def generate_file(self, ingredients, file_path):
        with open(MEDIA_ROOT / FILE_NAME, 'w') as file:
            for name, data in ingredients.items():
                file.write(
                    f'{name} ({data[MEASUREMENT_UNIT]}) — {data[AMOUNT]}\r\n'
                )

    @action(detail=False)
    def download_shopping_cart(self, request):
        ingredients = self.generate_shopping_cart_data(request)
        file_path = MEDIA_ROOT / FILE_NAME
        self.generate_file(ingredients, file_path)
        return FileResponse(open(file_path, 'rb'))
