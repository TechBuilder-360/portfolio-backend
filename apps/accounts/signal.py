"""
    Handles on save method for profile pix add or update action
    https://cloudinary.com/documentation/django_integration
"""
from random import random

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User


# Generates Username for new user
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def set_username(sender, instance=None, created=False, **kwargs):
#     if created:
#         username = instance.last_name + instance.first_name
#         while User.objects.filter(username=username).exists():
#             username += str(random.randint(123456, 999999))
#         instance.username = username
#         instance.save()
