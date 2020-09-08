from django.forms import ModelForm
from django import forms
from accounts.models import User
from resume.models import SocialLink, Education, Experience, Project, Skill, SubSkill


class SocialLinkForm(ModelForm):
    user_id = forms.IntegerField(required=True)

    class Meta:
        model = SocialLink
        exclude = ("user",)

    def save(self, commit=True):
        social = super().save(commit=False)
        user_id = self.cleaned_data["user_id"]
        user = User.objects.get(id=user_id)
        social.user = user
        if commit:
            return social.save()


class EducationForm(ModelForm):
    user_id = forms.IntegerField(required=True)

    class Meta:
        model = Education
        exclude = ("user", 'in_progress')

    def save(self, commit=True):
        education = super(EducationForm, self).save(commit=False)
        user_id = self.cleaned_data["user_id"]
        end_year = self.cleaned_data["end_year"]
        start_year = self.cleaned_data["start_year"]
        user = User.objects.get(id=user_id)
        if end_year:
            if end_year < start_year:
                raise forms.ValidationError("End date cannot be less than Start date")
            education.in_progress = False
        education.user = user
        if commit:
            education.save()


class ExperienceForm(ModelForm):
    user_id = forms.IntegerField(required=True)

    class Meta:
        model = Experience
        exclude = ("user", 'in_progress')

    def save(self, commit=True):
        experience = super(ExperienceForm, self).save(commit=False)
        user_id = self.cleaned_data["user_id"]
        end_year = self.cleaned_data["end_year"]
        start_year = self.cleaned_data["start_year"]
        user = User.objects.get(id=user_id)
        if end_year:
            if end_year < start_year:
                raise forms.ValidationError("End date cannot be less than Start date")
            experience.in_progress = False
        experience.user = user
        if commit:
            experience.save()


class ProjectForm(ModelForm):
    user_id = forms.IntegerField(required=True)

    class Meta:
        model = Project
        exclude = ("user",)

    def save(self, commit=True):
        project = super(ProjectForm, self).save(commit=False)
        user_id = self.cleaned_data["user_id"]
        user = User.objects.get(id=user_id)
        project.user = user
        if commit:
            project.save()
        return project


class SkillForm(ModelForm):
    user_id = forms.IntegerField(required=True)

    class Meta:
        model = Skill
        exclude = ("user",)

    def save(self, commit=True):
        skill = super(SkillForm, self).save(commit=False)
        user_id = self.cleaned_data["user_id"]
        title = self.cleaned_data["title"]
        user = User.objects.filter(id=user_id)
        if Skill.objets.filter(user=user, title=title).exists():
            return skill
        skill.user = user
        skill.save()
        if commit:
            return skill


class SubSkillForm(ModelForm):
    class Meta:
        model = SubSkill
        exclude = ("user",)
