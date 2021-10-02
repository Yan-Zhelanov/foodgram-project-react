from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    IntegerField,
    ImageField,
    ManyToManyField,
    Model,
    TextField,
    TimeField,
    SlugField,
    SET_NULL,
)
from django.urls import reverse
from django.contrib.auth import get_user_model

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

    def __str__(self):
        return f'{self.name}'


class Recipe(Model):
    name = CharField('Название', max_length=200)
    text = TextField('Описание')
    ingredients = ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты'
    )
    tags = ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    image = ImageField('Картинка')
    cooking_time = TimeField('Время приготовления')
    author = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.author}: {self.name}'

    def get_absoulute_url(self):
        return reverse('recepi', args=[self.pk])


class CountOfIngredient(Model):
    ingredient = ManyToManyField(
        Ingredient,
        verbose_name='Ингредиент',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт',
    )
    amount = IntegerField('Количество')

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.recipe}.{self.ingredient}'


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

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class ShoppingCart(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
    )
    recipes = ManyToManyField(
        Recipe,
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user}'
