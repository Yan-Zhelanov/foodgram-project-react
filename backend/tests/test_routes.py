from django.urls import reverse


def test_correct_routes():
    routes = [
        [reverse('users:users'), '/users'],
    ]
    for route in routes:
        assert route[0] == route[1]
