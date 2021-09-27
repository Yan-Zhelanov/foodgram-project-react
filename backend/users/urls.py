from django.urls import path, include

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls'), name='users'),
]
