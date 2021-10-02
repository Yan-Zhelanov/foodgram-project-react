import pytest

from django.urls import reverse


def test_correct_routes():
    routes = [
        [reverse('api:users:auth:login'), '/api/auth/token/login/'],
        [reverse('api:users:auth:logout'), '/api/auth/token/logout/'],
        [reverse('api:recipes:recipes'), '/api/recipes/'],
        [reverse('api:recipes:tags'), '/api/tags/'],
        [reverse('api:users:users'), '/api/users/'],
        
    ]
    for route in routes:
        assert route[0] == route[1], (
            'Неправильно настроен reverse'
        )
