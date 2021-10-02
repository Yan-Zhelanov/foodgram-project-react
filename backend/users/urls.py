from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('auth/', include(
        ('djoser.urls.authtoken', 'auth'), namespace='auth'
    )),
    path('', include(('djoser.urls', 'users'), namespace='users')),
]
