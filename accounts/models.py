from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager

SEX_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others')
)

AVAILABLE, UNAVAILABLE, DEACTIVATED = range(3)
STATUS_CHOICE = (
    (AVAILABLE, 'Available'),
    (UNAVAILABLE, 'Unavailable'),
    (DEACTIVATED, 'Deactivated')
)


class UserManager(BaseUserManager):
    def get_all_users(self):
        """Returns all users"""
        return super(UserManager, self).get_queryset().all()

    def get_active_users(self):
        """Returns all users"""
        return super(UserManager, self).get_queryset().filter(status=0)

    # Add Oauth Authentication later
    def create_user(self, last_name, first_name, email, password=None):
        user = self.model(
            last_name=last_name,
            first_name=first_name,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, last_name, first_name, middle_name, email, password):
        user = self.create_user(
            last_name, first_name, middle_name, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    first_name = models.CharField(verbose_name=_('First name'), max_length=50)
    last_name = models.CharField(verbose_name=_('Last name'), max_length=50)
    middle_name = models.CharField(verbose_name=_('Middle name'), max_length=50)
    email = models.EmailField(max_length=254, verbose_name=_('Email Address'), blank=False, null=False, unique=True)
    gender = models.CharField(max_length=10, choices=SEX_CHOICES, default='')
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.CharField(max_length=200)
    languages = models.CharField(max_length=100)
    resume = CloudinaryField('resume')
    nationality = models.CharField(max_length=20)
    state_of_residence = models.CharField(max_length=20)
    status = models.CharField(max_length=15, choices=STATUS_CHOICE, null=False, blank=False, default='Available')
    date_of_birth = models.DateField(null=True)  # applicant should be greater than 17
    profession = models.CharField(max_length=50, null=False, blank=False, default='')  # Todo: convert to choice field
    profile_pix = CloudinaryField('Profile picture')

    def __str__(self):
        return self.last_name + " " + self.first_name

    class Meta:
        app_label = 'accounts'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('first_name', 'last_name',)


class Social(models.Model):
    media = models.CharField(max_length=20, null=False, blank=False, unique=True)
    icon = CloudinaryField('Social icon')

    def __str__(self):
        return self.media


class SocialLink(models.Model):
    media = models.ForeignKey(User, on_delete=models.PROTECT)
    profile_url = models.URLField()

    def __str__(self):
        return str(self.media) + ' account'


PRIMARY, SECONDARY, TERTIARY, DIPLOMA = range(4)
EDUCATION_CHOICE = (
    (PRIMARY, "Primary"),
    (SECONDARY, 'Secondary'),
    (TERTIARY, 'Tertiary'),
    (DIPLOMA, 'Diploma')
)


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    education_type = models.CharField(max_length=20, choices=EDUCATION_CHOICE, null=False, blank=False)
    institution = models.CharField(max_length=100, null=False, blank=False)
    start_year = models.DateField()
    end_year = models.DateField()
    in_progress = models.BinaryField()
    degree = models.CharField(max_length=50)
    course = models.CharField(max_length=50, verbose_name=_('Discipline'))

    def __str__(self):
        return str(self.user) + " " + self.education_type


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    start_year = models.DateField()
    end_year = models.DateField()
    in_progress = models.BinaryField()

    def __str__(self):
        return str(self.user)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=50, null=False, blank=False)
    project_url = models.URLField()

    def __str__(self):
        return self.project_name[8]


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = CloudinaryField('Project Image')

    def __str__(self):
        return str(self.project)


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    # Todo: add icon

    def __str__(self):
        return self.title


class SubSkill(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    sub_skill = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.sub_skill
