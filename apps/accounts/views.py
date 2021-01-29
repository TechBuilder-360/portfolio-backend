import os
import cloudinary
import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection, EmailMessage
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template.response import TemplateResponse

from portfolio.settings import FRONTEND_URL, LOGOUT_REDIRECT_URL
from .forms import LoginForm, UploadForm
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
    try:
        context = dict({'user': user, 'link': FRONTEND_URL}, autoescape=False)
        subject = get_template('email/welcome_subject.txt').render(context)
        body = get_template('email/welcome_email_body.html').render(context)
        connection = get_connection()

        msg = EmailMessage(subject, body, to=[user.email], connection=connection)
        connection.send_messages([msg])  # Todo: Email send fails
    except:
        pass


def Login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, 'Incorrect login credential supplied')
    else:
        form = LoginForm()
    return TemplateResponse(request, 'index.html', {"form": form})


def logout_view(request):
    logout(request)
    return redirect(LOGOUT_REDIRECT_URL)


@login_required
def dashboard(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user, commit=False)
            messages.success(request, "File has been uploaded successfully")
            return redirect('dashboard')
    else:
        form = UploadForm()
    return TemplateResponse(request, 'accounts/dashboard.html', {'form': form})


@login_required
def download(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'sample.txt')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/txt")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
