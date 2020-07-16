from cloudinary.forms import CloudinaryFileField
from django.forms import forms

from resume.models import UserProfile


class AvatarUploadForm(forms.ModelForm):
    avatar = CloudinaryFileField(
        options = {
            'crop': 'thumb',
            'width': 200,
            'height': 200,
            'folder': 'avatars'
       }
    )
    class Meta:
        model = UserProfile
        fields = ('avatar',)