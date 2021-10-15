from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import TokenDestroyView

from .views import (
    ShoppingCartViewSet,
    UserSubscribeViewSet,
    TokenCreateWithCheckBlockStatusView
)

router = DefaultRouter()
router.register(r'users', UserSubscribeViewSet, basename='users')
router.register(r'recipes', ShoppingCartViewSet, basename='shopping_cart')

app_name = 'users'

authorization = [
    path(
        'token/login/',
        TokenCreateWithCheckBlockStatusView.as_view(),
        name="login",
    ),
    path('token/logout/', TokenDestroyView.as_view(), name="logout"),
]

urlpatterns = [
    path('auth/', include(authorization)),
    path('', include(router.urls)),
]
