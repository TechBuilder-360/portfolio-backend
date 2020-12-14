from datetime import datetime


def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    if kwargs.get('is_new', None):
        url = None
        if backend.name == 'facebook':
            url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
        if backend.name == 'twitter':
            url = response.get('profile_image_url', '').replace('_normal','')
        if backend.name == 'google-oauth2':
            url = response['picture']
            user.first_name = response['given_name']
            user.last_name = response['family_name']
            user.username = details['username']
        if url:
            user.profile_pix = url
            user.save()
    else:
        user.last_login = datetime.now()
