from django.contrib.admin import ModelAdmin, display, register

from foodgram.constants import EMPTY

from .models import (
    CountOfIngredient,
    Favorite,
    Ingredient,
    Recipe,
    Tag,
)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'color',)
    search_fields = ('name', 'slug',)
    ordering = ('color',)
    empty_value_display = EMPTY


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('measurement_unit',)
    empty_value_display = EMPTY


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('name', 'author', 'tags',)
    readonly_fields = ('added_in_favorites',)
    empty_value_display = EMPTY

    @display(description='Общее число добавлений в избранное')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


@register(CountOfIngredient)
class CountOfIngredientAdmin(ModelAdmin):
    list_display = (
        'recipe', 'ingredient', 'amount', 'get_measurement_unit'
    )
    readonly_fields = ('get_measurement_unit',)
    list_filter = ('recipe', 'ingredient',)
    ordering = ('recipe', 'ingredient',)
    empty_value_display = EMPTY

    @display(description='Единица измерения')
    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = EMPTY
