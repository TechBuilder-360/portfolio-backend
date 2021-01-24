from random import random, randint
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Template(models.Model):

    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    filename = models.CharField(max_length=20, blank=False, null=False, unique=True)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)], default=0)
    submitted_by = models.CharField(max_length=80, blank=False, null=False)
    creation_date = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.name


def set_username(instance):
    username = (instance.last_name + instance.first_name).lower()
    pre_exist = list(User.objects.filter(username__startswith=username).values_list('username', flat=True))
    while username in pre_exist:
        username += str(randint(1, 99999))
    return username


class UserManager(BaseUserManager):
    def create_user(self, last_name, first_name, email, password, username=None):
        user = self.model(
            last_name=last_name,
            first_name=first_name,
            email=self.normalize_email(email.lower())
        )
        user.username = set_username(user)
        user.set_password(password)
        user.save(using=self._db)
        user.status.verified = True
        user.status.save()
        return user

    def create_superuser(self, username, last_name, first_name, email, password):
        user = self.create_user(
            last_name, first_name, email, password, username)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    first_name = models.CharField(verbose_name=_('First name'), max_length=50, null=False, blank=False, default='')
    last_name = models.CharField(verbose_name=_('Last name'), max_length=50, null=False, blank=False, default='')
    middle_name = models.CharField(verbose_name=_('Middle name'), max_length=50, blank=True, null=True, default='')
    email = models.EmailField(max_length=254, verbose_name=_('Email Address'), blank=False, null=False, unique=True)
    gender = models.CharField(max_length=10, default='', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True, default='')
    bio = models.TextField(max_length=500, help_text="Professional Summary", null=True, blank=True, default='')
    languages = models.CharField(max_length=100, help_text="Languages", null=True, blank=True, default='')
    template = models.ForeignKey(Template, null=True, on_delete=models.PROTECT, related_name='template')
    location = models.CharField(max_length=70, null=True, blank=True, default='')
    date_of_birth = models.DateField(null=True, blank=True)  # applicant should be greater than 17
    profession = models.CharField(max_length=50, verbose_name=_("Job Title"), null=True, blank=True, default='')  # Todo: convert to choice field
    profile_pix = models.URLField('avatar', null=True, blank=True, default='')
    allow_download = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)

    manager = UserManager()

    def __str__(self):
        return "(%d) - %s %s" % (self.id, self.last_name, self.first_name)

    class Meta:
        app_label = 'accounts'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('first_name',)

    def get_full_name(self):
        return "%s, %s %s" % (self.last_name, self.first_name, self.middle_name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.username = set_username(self)
        return super(User, self).save(*args, **kwargs)


class Contact(models.Model):
    email = models.EmailField(_("Email Address"), null=False, blank=False)
    full_name = models.CharField(max_length=80, null=False, blank=False)
    message = models.CharField(max_length=255, null=False, blank=False)
    created_on = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return "(%s: %s)" % (self.full_name[:10], self.message[:15])



