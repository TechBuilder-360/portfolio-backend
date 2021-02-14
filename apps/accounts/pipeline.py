import uuid
from datetime import datetime

from .models import User


def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    if kwargs.get('is_new', None):
        url = None
        if backend.name == 'google-oauth2':
            url = response['picture']
            user.first_name = response['given_name']
            user.last_name = response['family_name']
            user.username = details['username']
            if User.objects.filter(username=details['username']).exists():
                user.username += str(uuid.uuid4()).replace('-', '')[:8]
            user.last_login = datetime.now()
            user.status.verified = True
            user.status.save()
            user.save()
        if url:
            user.profile_pix = url
    else:
        user.last_login = datetime.now()
