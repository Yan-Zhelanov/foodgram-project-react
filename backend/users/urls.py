from django.urls import include, path

app_name = 'users'

urlpatterns = [
    path('auth/', include(
        ('djoser.urls.authtoken', 'auth'), namespace='auth'
    )),
    path('', include('djoser.urls')),
]
