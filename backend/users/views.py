from django.db import IntegrityError
from django.db.models import Sum
from django.http import FileResponse, Http404
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
    HTTP_404_NOT_FOUND
)
from rest_framework.viewsets import GenericViewSet
from djoser.views import TokenCreateView

from foodgram.constants import ERRORS_KEY
from foodgram.pagination import LimitPageNumberPagination
from foodgram.settings import MEDIA_ROOT
from recipes.models import Recipe
from recipes.serializers import RecipeShortReadSerializer

from .models import ShoppingCart, Subscribe, User
from .serializers import SubscriptionSerializer

FILE_NAME = 'shopping_cart.txt'

SUBSCRIBE_CANNOT_CREATE_TO_YOURSELF = 'Нельзя подписаться на самого себя!'
SUBSCRIBE_CANNOT_CREATE_TWICE = 'Нельзя подписаться дважды!'
SUBSCRIBE_CANNOT_DELETE = (
    'Нельзя отписаться от данного пользователя,'
    ' если вы не подписаны на него!'
)

USER_BLOCKED = 'Данный аккаунт временно заблокирован!'
USER_NOT_FOUND = 'Пользователь не найден!'

SHOPPING_CART_DOES_NOT_EXISTS = 'Список покупок не существует!'
SHOPPING_CART_RECIPE_CANNOT_ADDED_TWICE = 'Рецепт уже добавлен!'
SHOPPING_CART_RECIPE_CANNOT_DELETE = (
    'Нельзя удалить рецепт из списка покупок, которого нет'
    ' в списке покупок!'
)


class TokenCreateWithCheckBlockStatusView(TokenCreateView):
    def _action(self, serializer):
        if serializer.user.is_blocked:
            return Response(
                {ERRORS_KEY: USER_BLOCKED},
                status=HTTP_400_BAD_REQUEST,
            )
        return super()._action(serializer)


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
                {ERRORS_KEY: SUBSCRIBE_CANNOT_CREATE_TO_YOURSELF},
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            subscribe = Subscribe.objects.create(
                user=request.user,
                author=author,
            )
        except IntegrityError:
            return Response(
                {ERRORS_KEY: SUBSCRIBE_CANNOT_CREATE_TWICE},
                status=HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_subscribtion_serializer(subscribe.author)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete_subscribe(self, request, author):
        try:
            Subscribe.objects.get(user=request.user, author=author).delete()
        except Subscribe.DoesNotExist:
            return Response(
                {ERRORS_KEY: SUBSCRIBE_CANNOT_DELETE},
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
                {'detail': USER_NOT_FOUND},
                status=HTTP_404_NOT_FOUND,
            )
        if request.method == 'GET':
            return self.create_subscribe(request, author)
        return self.delete_subscribe(request, author)


class ShoppingCartViewSet(GenericViewSet):
    NAME = 'ingredients__ingredient__name'
    MEASUREMENT_UNIT = 'ingredients__ingredient__measurement_unit'
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeShortReadSerializer
    queryset = ShoppingCart.objects.all()
    http_method_names = ('get', 'delete',)

    def generate_shopping_cart_data(self, request):
        recipes = (
            request.user.shopping_cart.recipes.prefetch_related('ingredients')
        )
        return (
            recipes.order_by(self.NAME)
            .values(self.NAME, self.MEASUREMENT_UNIT)
            .annotate(total=Sum('ingredients__amount'))
        )

    def generate_file(self, ingredients, file_path):
        with open(
            MEDIA_ROOT / f'{FILE_NAME}-{self.request.user.pk}',
            'w',
            encoding='utf-8',
        ) as file:
            for ingredient in ingredients:
                file.write(
                    f'{ingredient[self.NAME]}'
                    f' ({ingredient[self.MEASUREMENT_UNIT]})'
                    f' — {ingredient["total"]}\r\n'
                )

    @action(detail=False)
    def download_shopping_cart(self, request):
        try:
            ingredients = self.generate_shopping_cart_data(request)
        except ShoppingCart.DoesNotExist:
            return Response(
                {ERRORS_KEY: SHOPPING_CART_DOES_NOT_EXISTS},
                status=HTTP_400_BAD_REQUEST
            )
        file_path = MEDIA_ROOT / FILE_NAME
        self.generate_file(ingredients, file_path)
        return FileResponse(open(file_path, 'rb'))

    def add_to_shopping_cart(self, request, recipe, shopping_cart):
        if shopping_cart.recipes.filter(pk__in=(recipe.pk,)).exists():
            return Response(
                {ERRORS_KEY: SHOPPING_CART_RECIPE_CANNOT_ADDED_TWICE},
                status=HTTP_400_BAD_REQUEST,
            )
        shopping_cart.recipes.add(recipe)
        serializer = self.get_serializer(recipe)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
        )

    def remove_from_shopping_cart(self, request, recipe, shopping_cart):
        if not shopping_cart.recipes.filter(pk__in=(recipe.pk,)).exists():
            return Response(
                {ERRORS_KEY: SHOPPING_CART_RECIPE_CANNOT_DELETE},
                status=HTTP_400_BAD_REQUEST,
            )
        shopping_cart.recipes.remove(recipe)
        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    @action(methods=('get', 'delete',), detail=True)
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_cart = (
            ShoppingCart.objects.get_or_create(user=request.user)[0]
        )
        if request.method == 'GET':
            return self.add_to_shopping_cart(request, recipe, shopping_cart)
        return self.remove_from_shopping_cart(request, recipe, shopping_cart)
