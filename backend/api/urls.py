from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('', include('users.urls', namespace='users')),
    path('', include('recipes.urls', namespace='recipes')),
]