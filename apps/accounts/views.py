import cloudinary
import jwt
from django.conf import settings
from django.core.mail import get_connection, EmailMessage
from django.http import JsonResponse
from django.template.loader import get_template

from .models import User


def avartar(request):
    encoded_jwt = request.headers.get('Authorization')
    decoded_jwt = jwt.decode(encoded_jwt.split()[1], settings.SECRET_KEY, algorithms=['HS256'])
    image = cloudinary.uploader.upload(request.FILES['image'],
                                       folder="xportfolio/profile_pix/",
                                       public_id=decoded_jwt['username'],
                                       overwrite=True,
                                       resource_type="image"
                                       )
    User.objects.filter(username=decoded_jwt['username']).update(profile_pix=image['url'])
    return JsonResponse({'url': image['url']})


def welcome_mail(user):
    context = dict({'user': user}, autoescape=False)
    subject = get_template('email/welcome_subject.txt').render(context)
    body = get_template('email/welcome_email_body.txt').render(context)
    connection = get_connection()

    msg = EmailMessage(subject, body, to=[user.email], connection=connection)
    connection.send_messages([msg])
