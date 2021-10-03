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
        return len(
            obj.subscribing.filter(user=self.context['request'].user)
        ) == 1