from django.forms import ModelForm
from resume.models import SocialLink, Education, Experience, Project, Skill, SubSkill


class SocialLinkForm(ModelForm):
    class Meta:
        model = SocialLink
        exclude = ("user",)


class EducationForm(ModelForm):
    class Meta:
        model = Education
        exclude = ("user",)


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        exclude = ("user",)


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ("user",)


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ("user",)


class SubSkillForm(ModelForm):
    class Meta:
        model = SubSkill
        exclude = ("user",)
