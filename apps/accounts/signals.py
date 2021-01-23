from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .views import welcome_mail


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        welcome_mail(instance)
