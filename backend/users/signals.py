from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, ShoppingCart

@receiver(post_save, sender=User)
def create_shopping_cart(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(user=instance)
