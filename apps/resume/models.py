from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User


class SocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    label = models.CharField(max_length=20, verbose_name=_("Social host i.e Facebook, twitter etc."))
    profile_url = models.URLField()

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
    education_type = models.CharField(max_length=20, choices=EDUCATION_CHOICE, null=False, blank=False)
    institution = models.CharField(max_length=100, null=False, blank=False)
    start_year = models.DateField()
    end_year = models.DateField(null=True, blank=True)
    in_progress = models.BooleanField(
        default=True)  # TODO: a checker should be set to change in_progress to false if end date is a future date
    degree = models.CharField(max_length=50, null=False, blank=False)
    course = models.CharField(max_length=50, verbose_name=_('Discipline'), null=False, blank=False)

    def __str__(self):
        return str(self.user) + " " + self.education_type


class Experience(models.Model):  # Employment History
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    start_year = models.DateField()
    end_year = models.DateField(null=True)
    in_progress = models.BooleanField(default=True)  # True if end date is not specified

    def __str__(self):
        return str(self.user) + "(" + self.title[20] + ")"


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=50, null=False, blank=False)
    project_url = models.URLField()  # TODO Add option to fetch content of url i.e pull github project details

    def __str__(self):
        return str(self.user) + "(" + self.project_name[20] + ")"


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class SubSkill(models.Model):  # Still rethinking of the relevance of this model. To remove or not to
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    sub_skill = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.sub_skill
