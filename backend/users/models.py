from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    EmailField,
    ForeignKey,
    ManyToManyField,
    Model,
    OneToOneField,
)

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = EmailField(max_length=254, unique=True)
    username = CharField(max_length=150)
    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150)
    password = CharField(max_length=150)
    is_superuser = BooleanField(default=False)
    is_blocked = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser


class Subscribe(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'author',)

    def __str__(self):
        return f'{self.user} -> {self.author}'


class ShoppingCart(Model):
    user = OneToOneField(
        User,
        on_delete=CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipes = ManyToManyField(
        'recipes.Recipe',
        related_name='in_shopping_cart',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user}'
