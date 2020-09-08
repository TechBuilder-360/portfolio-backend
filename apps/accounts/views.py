from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.response import TemplateResponse


def index(request):
    return TemplateResponse(request, 'accounts/google_auth.html')


@login_required()
def dashboard(request):
    return TemplateResponse(request, 'accounts/dashboard.html')


def userLogin(request):
    if request.method == 'GET':
        username = 'Adegunwa'
        password = '1234567890'
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['Token'] = "djhgfjkbjvdcfhbmdsgdjsfjhdf"
                # logout(request)
                return HttpResponse(status=200, content="OK :)")
            else:
                return HttpResponse("Your account was inactive.", status=202)
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return HttpResponse(status=400)
