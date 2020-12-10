from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User


class SocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=20, verbose_name=_("Social host i.e Facebook, twitter etc."))
    social_url = models.URLField()

    def __str__(self):
        return self.label


PRIMARY, SECONDARY, TERTIARY, DIPLOMA = range(4)
EDUCATION_CHOICE = (
    (PRIMARY, "Primary"),
    (SECONDARY, 'Secondary'),
    (TERTIARY, 'Tertiary'),
    (DIPLOMA, 'Diploma')
)


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100, null=False, blank=False)
    start_year = models.CharField(max_length=9, null=False, blank=False)
    end_year = models.CharField(max_length=9, null=False, blank=False)
    degree = models.CharField(max_length=50, null=False, blank=False)
    course = models.CharField(max_length=50, verbose_name=_('Discipline'), null=False, blank=False)

    def __str__(self):
        return str(self.user)


class Experience(models.Model):  # Employment History
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=50, null=False, blank=False)
    position = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    start_year = models.CharField(max_length=9, null=False, blank=False)
    end_year = models.CharField(max_length=9, null=False, blank=False)

    def __str__(self):
        return str(self.user) + "(" + self.organization[:20] + ")"


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_url = models.URLField()
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.title


class SubSkill(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='sub_skills')
    title = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.title
