from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Пользователи'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import users.signals
