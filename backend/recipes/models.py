from django.db.models import (
    Model,
    ManyToManyField,
    ImageField,
    CharField,
    TextField,
    ForeignKey,
    TimeField,
    SlugField,
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


class Recipe(Model):
    name = CharField('Название', max_length=200)
    text = TextField('Описание')
    ingredients = ManyToManyField('Ингредиенты')
    tags = ManyToManyField('Теги')
    image = ImageField('Картинка')
    cooking_time = TimeField('Время приготовления')
    author = ForeignKey(
        User,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.author.username}: {self.name}'

    def get_absoulute_url(self):
        return reverse('recepi', args=[self.pk])
