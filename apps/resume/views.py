from django.shortcuts import get_object_or_404
from accounts.models import User
from .models import Education, Experience, Skill, Project, Accomplishment
from portfolio.utils.pdf import PdfResponse


def resume_download(request, username):
    user = get_object_or_404(User, username=username)
    params = {
        'user': user,
        'educations': Education.objects.filter(user=user),
        'experiences': Experience.objects.filter(user=user),
        'skills': Skill.objects.filter(user=user),
        'projects': Project.objects.filter(user=user),
        'accomplishments': Accomplishment.objects.filter(user=user)
    }
    template = user.template.filename if user.template.filename else 'template'
    return PdfResponse(request, 'resume/%s.html' % template, params, filename='resume')
