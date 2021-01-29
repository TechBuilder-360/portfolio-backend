from datetime import datetime

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import User
from .views import welcome_mail


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        welcome_mail(instance)


@receiver(pre_save, sender=User)
def set_last_login(sender, instance, **kwargs):
    instance.is_new = False
    instance.last_login = datetime.now()
