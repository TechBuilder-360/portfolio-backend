from django.forms import ModelForm
from django import forms
from accounts.models import User
from resume.models import Education, Experience


class EducationForm(ModelForm):
    id = forms.IntegerField(required=False)

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
    id = forms.IntegerField(required=False)

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
