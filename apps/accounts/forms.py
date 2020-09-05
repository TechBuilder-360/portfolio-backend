import uuid

from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm
from django import forms
from .models import User


class RegistrationForm(ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_password(self):
        """
            Check that the password entries is valid
        """
        password = self.cleaned_data.get("password")
        validate_password(password=password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = uuid.uuid4()
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class PersonalInformationForm(ModelForm):

    user_id = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'gender', 'phone', 'bio',
                  'languages', 'nationality', 'state_of_residence', 'status', 'date_of_birth', 'profession')

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        # TODO add method to move uploaded file to cloudinary
        return avatar

    def clean_resume(self):
        resume = self.cleaned_data.get("resume")
        # TODO add method to move uploaded file to cloudinary
        return resume


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(max_length=15)
    password = forms.CharField(max_length=15)
    confirm_password = forms.CharField(max_length=15)
    user_id = forms.IntegerField(required=True)

    def clean_user_id(self):
        user_id = self.cleaned_data.get("user_id")
        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise forms.ValidationError("User does not Exist")

    def clean_old_password(self):
        """
            Check that old password matches current password
        """
        old_password = self.cleaned_data.get("old_password")
        user_id = self.cleaned_data.get("id")
        user = User.objects.get(id=user_id)
        if not user.check_password(raw_password=old_password):
            raise forms.ValidationError("Old password is incorrect")
        return old_password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if not password or not confirm_password:
            raise forms.ValidationError("Password field cannot be empty")
        password = password.trim()
        if password != confirm_password:
            raise forms.ValidationError("Confirm Password does not match")
        return password

    def save(self, commit=True):
        form = super().save(commit=False)
        user = User.objects.get(id=self.cleaned_data["user_id"])
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

