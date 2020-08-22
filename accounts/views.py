from django.template.response import TemplateResponse


def index(request):
    if request.user.is_authenticated:
        print(request.user)
    return TemplateResponse(request, 'accounts/google_auth.html')
