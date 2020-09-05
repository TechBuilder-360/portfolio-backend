from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse


def index(request):
    return TemplateResponse(request, 'accounts/google_auth.html')


@login_required()
def dashboard(request):
    return TemplateResponse(request, 'accounts/dashboard.html')
