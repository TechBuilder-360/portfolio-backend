from django import forms
from django.forms import ModelForm

from .models import Template


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))


class UploadForm(ModelForm):

    class Meta:
        model = Template
        fields = ('name', 'file')

    def save(self, user, commit=True):
        template = super(UploadForm, self).save(commit=False)
        template.submitted_by = user.get_full_name()
        template.save()

