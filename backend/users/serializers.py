from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import User


class UserSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField('is_subscribed_user')

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )
        read_only_fields = ('is_subscribed',)

    # TODO: Перенести бизнес-логику в services.py
    def is_subscribed_user(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and obj.subscribing.filter(user=user).exists()
        )


class SubscriptionSerializer(UserSerializer):
    from recipes.serializers import RecipeShortReadSerializer
    recipes = RecipeShortReadSerializer(many=True)
    recipes_count = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count',)

    def get_recipes_count(self, obj):
        return obj.recipes.count()
