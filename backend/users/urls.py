from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ShoppingCartViewSet, UserSubscribeViewSet

router = DefaultRouter()
router.register(r'users', UserSubscribeViewSet, basename='users')
router.register(r'recipes', ShoppingCartViewSet, basename='shopping_cart')

app_name = 'users'

urlpatterns = [
    path(
        'auth/',
        include(
            ('djoser.urls.authtoken', 'auth'),
            namespace='auth'
        )
    ),
    path('', include(router.urls)),
]
