from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import BooleanFilter

from .models import Recipe


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def get_is_favorited(self, queryset, name, value):
        favorites = self.request.user.favorites.all()
        return queryset.filter(
            pk__in=(favorite.recipe.pk for favorite in favorites)
        )

    def get_is_in_shopping_cart(self, queryset, name, value):
        recipes = (
            self.request.user.shopping_cart.recipes.all()
        )
        return queryset.filter(
            pk__in=(recipe.pk for recipe in recipes)
        )