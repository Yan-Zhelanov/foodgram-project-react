from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ListField,
    ModelSerializer,
    SerializerMethodField,
    SlugRelatedField,
    ValidationError
)

from foodgram.constants import COOKING_TIME_MIN_VALUE, INGREDIENT_MIN_AMOUNT
from recipes.models import (
    COOKING_TIME_MIN_ERROR,
    CountOfIngredient,
    Ingredient,
    Recipe,
    Tag
)
from users.models import ShoppingCart
from users.serializers import UserSerializer

TAGS_UNIQUE_ERROR = 'Теги не могут повторяться!'
TAGS_EMPTY_ERROR = 'Рецепт не может быть без тегов!'
INGREDIENTS_UNIQUE_ERROR = 'Ингредиенты не могут повторяться!'
INGREDIENTS_EMPTY_ERROR = 'Без ингредиентов рецепта не бывает!'
INGREDIENT_MIN_AMOUNT_ERROR = (
    'Количество ингредиента не может быть меньше {min_value}!'
)
INGREDIENT_DOES_NOT_EXIST = 'Такого ингредиента не существует!'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientWriteSerializer(ModelSerializer):
    class Meta:
        model = CountOfIngredient
        fields = ('id', 'amount',)
        extra_kwargs = {
            'id': {
                'read_only': False,
                'error_messages': {
                    'does_not_exist': INGREDIENT_DOES_NOT_EXIST,
                }
            },
            'amount': {
                'error_messages': {
                    'min_value': INGREDIENT_MIN_AMOUNT_ERROR.format(
                        min_value=INGREDIENT_MIN_AMOUNT
                    ),
                }
            }
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

    def get_user(self):
        return self.context['request'].user

    def get_is_favorited(self, obj):
        user = self.get_user()
        return (
            user.is_authenticated
            and user.favorites.filter(recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.get_user()
        try:
            return (
                user.is_authenticated and
                user.shopping_cart.recipes.filter(pk__in=(obj.pk,)).exists()
            )
        except ShoppingCart.DoesNotExist:
            return False


class RecipeWriteSerializer(ModelSerializer):
    ingredients = RecipeIngredientWriteSerializer(many=True)
    tags = ListField(
        child=SlugRelatedField(
            slug_field='id',
            queryset=Tag.objects.all(),
        ),
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',
        )
        extra_kwargs = {
            'cooking_time': {
                'error_messages': {
                    'min_value': COOKING_TIME_MIN_ERROR,
                }
            }
        }

    def validate(self, attrs):
        if attrs['cooking_time'] < COOKING_TIME_MIN_VALUE:
            raise ValidationError(COOKING_TIME_MIN_ERROR)
        if len(attrs['tags']) == 0:
            raise ValidationError(TAGS_EMPTY_ERROR)
        if len(attrs['tags']) > len(set(attrs['tags'])):
            raise ValidationError(TAGS_UNIQUE_ERROR)
        if len(attrs['ingredients']) == 0:
            raise ValidationError(INGREDIENTS_EMPTY_ERROR)
        id_ingredients = []
        for ingredient in attrs['ingredients']:
            if ingredient['amount'] < INGREDIENT_MIN_AMOUNT:
                raise ValidationError(
                    INGREDIENT_MIN_AMOUNT_ERROR.format(
                        id=ingredient['id'],
                        min_value=INGREDIENT_MIN_AMOUNT,
                    )
                )
            id_ingredients.append(ingredient['id'])
        if len(id_ingredients) > len(set(id_ingredients)):
            raise ValidationError(INGREDIENTS_UNIQUE_ERROR)
        return attrs

    def add_ingredients_and_tags(self, instance, validated_data):
        ingredients, tags = (
            validated_data.pop('ingredients'), validated_data.pop('tags')
        )
        for ingredient in ingredients:
            count_of_ingredient, _ = CountOfIngredient.objects.get_or_create(
                ingredient=get_object_or_404(Ingredient, pk=ingredient['id']),
                amount=ingredient['amount'],
            )
            instance.ingredients.add(count_of_ingredient)
        for tag in tags:
            instance.tags.add(tag)
        return instance

    def create(self, validated_data):
        saved = {}
        saved['ingredients'] = validated_data.pop('ingredients')
        saved['tags'] = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        return self.add_ingredients_and_tags(recipe, saved)

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        instance = self.add_ingredients_and_tags(instance, validated_data)
        return super().update(instance, validated_data)
