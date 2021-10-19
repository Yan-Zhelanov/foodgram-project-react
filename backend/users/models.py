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
    UniqueConstraint
)

from .managers import UserManager

SHOPPING_CART_RECIPE_ALREADY_EXISTS_ERROR = (
    'Данный рецепт уже есть в вашем списке покупок!'
)


class User(AbstractBaseUser, PermissionsMixin):
    email = EmailField('Почта', max_length=254, unique=True)
    username = CharField('Никнейм', max_length=150)
    first_name = CharField('Имя', max_length=150)
    last_name = CharField('Фамилия', max_length=150)
    password = CharField('Пароль', max_length=150)
    is_superuser = BooleanField('Администратор', default=False)
    is_blocked = BooleanField('Заблокирован', default=False)

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
        constraints = (
            UniqueConstraint(
                fields=('user', 'author',),
                name='unique_subscribe',
            ),
        )

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
