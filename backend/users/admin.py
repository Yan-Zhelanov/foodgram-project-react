from django.contrib.admin import ModelAdmin, display, register
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count, Sum

from foodgram.constants import EMPTY
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import ShoppingCart, Subscribe, User


@register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'is_blocked',
        'is_superuser',
    )
    list_filter = (
        'email', 'username', 'is_blocked', 'is_superuser',
    )
    fieldsets = (
        (None, {'fields': (
            'email', 'username', 'first_name', 'last_name', 'password',
        )}),
        ('Permissions', {'fields': ('is_blocked', 'is_superuser',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'password1',
                'password2', 'is_blocked', 'is_superuser',
            )
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    ordering = ('id', 'email', 'username',)


@register(Subscribe)
class SubscribeAdmin(ModelAdmin):
    list_display = ('user', 'author',)
    empty_value_display = EMPTY

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('user', 'count_ingredients',)
    readonly_fields = ('count_ingredients',)
    empty_value_display = EMPTY

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    @display(description='Количество ингредиентов')
    def count_ingredients(self, obj):
        return (
            obj.recipes.all().annotate(count_ingredients=Count('ingredients'))
            .aggregate(total=Sum('count_ingredients'))['total']
        )
