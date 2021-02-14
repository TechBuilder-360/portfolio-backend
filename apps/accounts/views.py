import os
import cloudinary
import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection, EmailMessage
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template
from django.template.response import TemplateResponse
from portfolio.settings import FRONTEND_URL, LOGOUT_REDIRECT_URL
from .forms import LoginForm, UploadForm
from .models import User, Template
import logging

logger = logging.getLogger('__name__')


def avartar(request):
    encoded_jwt = request.headers.get('Authorization')
    decoded_jwt = jwt.decode(encoded_jwt.split()[1], settings.SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(email=decoded_jwt['email'])
    image = cloudinary.uploader.upload(request.FILES['image'],
                                       folder="oris/profile_pix/",
                                       public_id=user.username,
                                       overwrite=True,
                                       resource_type="image"
                                       )
    user.profile_pix = image['url']
    user.save()
    return JsonResponse({'url': image['url']})


def welcome_mail(user):
    try:
        context = dict({'user': user, 'link': FRONTEND_URL}, autoescape=False)
        subject = get_template('email/welcome_subject.txt').render(context)
        body = get_template('email/welcome_email_body.html').render(context)
        connection = get_connection()

        msg = EmailMessage(subject, body, to=[user.email], connection=connection)
        connection.send_messages([msg])  # Todo: Email send fails
    except Exception as ex:
        logger.error("Welcome email failed to send!\nError: %s" % ex)
        pass


def Login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            try:
                usr = User.objects.get(email__iexact=email).username
                if usr:
                    password = request.POST.get('password')
                    user = authenticate(request, username=usr, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect("dashboard")
            except:
                logger.error("User with email address %s not found" % email)
            messages.error(request, 'Incorrect login credential supplied')
    else:
        form = LoginForm()
    return TemplateResponse(request, 'index.html', {"form": form})


def logout_view(request):
    logout(request)
    return redirect(LOGOUT_REDIRECT_URL)


@login_required
def dashboard(request, pk=None):
    instance = get_object_or_404(Template, pk=pk) if pk else None
    if request.method == 'POST':
        form = UploadForm(instance=instance, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(user=request.user, commit=False)
            messages.success(request, "File has been uploaded successfully")
            return redirect('dashboard')
    else:
        templates = Template.objects.all()
        form = UploadForm(instance=instance)
    return TemplateResponse(request, 'accounts/dashboard.html', {'form': form, 'templates': templates})


@login_required
def download(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'sample.txt')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/txt")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
