from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    ForeignKey,
    ImageField,
    ManyToManyField,
    Model,
    PositiveIntegerField,
    SlugField,
    TextField
)
from django.urls import reverse

User = get_user_model()


class Tag(Model):
    name = CharField('Название', max_length=200)
    color = CharField('Цвет в HEX', max_length=7)
    slug = SlugField('Слаг', max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('tag', args=[self.slug])


class Ingredient(Model):
    name = CharField('Название', max_length=200)
    measurement_unit = CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Recipe(Model):
    name = CharField('Название', max_length=200)
    text = TextField('Описание')
    ingredients = ManyToManyField(
        'CountOfIngredient',
        related_name='recipe',
        verbose_name='Ингредиенты'
    )
    tags = ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    image = ImageField('Картинка')
    cooking_time = PositiveIntegerField(
        'Время приготовления',
        validators=(MinValueValidator(1),)
    )
    author = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name} ({self.author})'

    def get_absoulute_url(self):
        return reverse('recipe', args=[self.pk])


class CountOfIngredient(Model):
    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        related_name='count_in_recipes',
        verbose_name='Ингредиент',
    )
    amount = PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        unique_together = ('ingredient', 'amount',)

    def __str__(self):
        return (
            f'{self.ingredient.name} - {self.amount}'
            f' ({self.ingredient.measurement_unit})'
        )


class Favorite(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'recipe',)

    def __str__(self):
        return f'{self.user} -> {self.recipe}'
