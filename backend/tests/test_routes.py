from django.urls import reverse


def test_correct_routes():
    routes = [
        [reverse('recipes:recipes'), '/api/recipes/'],
    ]
    for route in routes:
        assert route[0] == route[1]
