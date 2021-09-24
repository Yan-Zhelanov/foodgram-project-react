from django.contrib.auth.models import AbstractBaseUser
from django.db.models import EmailField, CharField, BooleanField

from .managers import UserManager


class User(AbstractBaseUser):
    email = EmailField(max_length=254, unique=True)
    username = CharField(max_length=150)
    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150)
    password = CharField(max_length=150)
    is_superuser = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
    
