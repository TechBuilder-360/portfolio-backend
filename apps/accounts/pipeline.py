from datetime import datetime
# from accounts.views import welcome_mail


def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    if kwargs.get('is_new', None):
        url = None
        # if backend.name == 'facebook':
        #     url = "http://graph.facebook.com/%s/picture?type=large" % (response['id'])
        # if backend.name == 'twitter':
        #     url = response.get('profile_image_url', '').replace('_normal', '')
        if backend.name == 'google-oauth2':
            url = response['picture']
            user.first_name = response['given_name']
            user.last_name = response['family_name']
            user.username = details['username']
            user.last_login = datetime.now()
            user.status.verified = True
            user.status.save()
        if url:
            user.profile_pix = url
            # welcome_mail(user)
    else:
        user.last_login = datetime.now()
    user.save()
