from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    SlugRelatedField,
    ListField,
    SerializerMethodField,
)

from users.serializers import UserSerializer

from .models import CountOfIngredient, Recipe, Tag, Ingredient


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class RecipeIngredientWriteSerializer(ModelSerializer):
    class Meta:
        model = CountOfIngredient
        fields = ('id', 'amount',)
        extra_kwargs = {
            'id': {
                'read_only': False,
            },
        }


class RecipeIngredientReadSerializer(ModelSerializer):
    id = IntegerField(source='ingredient.id') # noqa
    name = CharField(source='ingredient.name')
    measurement_unit = CharField(source='ingredient.measurement_unit')

    class Meta:
        model = CountOfIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeReadSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = RecipeIngredientReadSerializer(many=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'image', 'text', 'cooking_time',
        )

    # TODO: переделать на exists
    def get_is_favorited(self, obj):
        return len(
            self.context['request'].user.favorites.filter(recipe=obj)
        ) == 1

    def get_is_in_shopping_cart(self, obj):
        return len(
            self.context['request'].user.shopping_cart.recipes
                .filter(pk__in=(obj.pk,))
        ) == 1


class RecipeWriteSerializer(ModelSerializer):
    ingredients = RecipeIngredientWriteSerializer(many=True)
    tags = ListField(
        child=SlugRelatedField(
            slug_field='id',
            queryset=Tag.objects.all()
        )
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags', 'image', 'name', 'text', 'cooking_time',
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            count_of_ingredient = CountOfIngredient.objects.create(
                ingredient=get_object_or_404(Ingredient, pk=ingredient['id']),
                amount=ingredient['amount'],
            )
            recipe.ingredients.add(count_of_ingredient)
        for tag in tags:
            recipe.tags.add(tag)
        return RecipeReadSerializer(instance=recipe).data
