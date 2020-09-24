import cloudinary
from django.forms import ModelForm
from django import forms
from .models import User, Contact


class PersonalInformationForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'gender', 'phone', 'bio',
                  'languages', 'nationality', 'state_of_residence', 'date_of_birth', 'profession')


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('email', 'full_name', 'message')

# cloudinary.uploader.upload('~/Downloads/image.jpeg')