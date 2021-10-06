from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.serializers import UserSerializer

from .models import Ingredient, Recipe, Tag, CountOfIngredient


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class CountOfIngredientSerializer(ModelSerializer):
    class Meta:
        model = CountOfIngredient
        fields = ('amount')


class IngredientCountSerializer(ModelSerializer):
    amount = SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_amount(self, obj):
        wtf = CountOfIngredient.objects.get(
            ingredient=obj.pk,
            recipe=self.context['recipe'],
        ).amount
        return wtf


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'image', 'text', 'cooking_time',
        )

    def get_ingredients(self, obj):
        return IngredientCountSerializer(
            instance=obj.ingredients,
            many=True
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
