from django.forms import ModelForm
from .models import User, Contact


class PersonalInformationForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'gender', 'phone', 'bio', 'email',
                  'languages', 'location', 'date_of_birth', 'profession')

    def save(self, commit=True):
        personal = super(PersonalInformationForm, self).save(commit=False)
        personal.save()
        return personal


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('email', 'full_name', 'message')

# cloudinary.uploader.upload('~/Downloads/image.jpeg')