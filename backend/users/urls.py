from django.urls import include, path

from .views import SubscribeAPIView

app_name = 'users'

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscribeAPIView.as_view(),
        name='subscriptions'
    ),
    path(
        'auth/',
        include(
            ('djoser.urls.authtoken', 'auth'),
            namespace='auth'
        )
    ),
    path('', include('djoser.urls')),
]
