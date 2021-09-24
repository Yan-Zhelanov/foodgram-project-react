from django.urls import path, include

urlpatterns = [
    path('auth/token/', include('djoser.urls.jwt')),
    path('users/', include('djoser.urls')),
]
