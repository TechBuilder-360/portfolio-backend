from urllib import request as req
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from accounts.models import User
from django.template import Template, Context
from .models import Education, Experience, Skill, Project, Accomplishment, SocialLink
from django_xhtml2pdf.utils import pdf_decorator


@pdf_decorator(pdfname='new_filename.pdf')
def resume_download(request, username):
    user = get_object_or_404(User, username=username)
    params = {
        'user': user,
        'educations': Education.objects.filter(user=user),
        'experiences': Experience.objects.filter(user=user),
        'skills': Skill.objects.filter(user=user),
        'projects': Project.objects.filter(user=user),
        'accomplishments': Accomplishment.objects.filter(user=user),
        'social': SocialLink.objects.filter(user=user)
    }

    try:
        user.template.file.file
        user = get_object_or_404(User, username=username)
        tpl_html = req.urlopen(user.template.file.url)
        data = tpl_html.read()
        text = data.decode('utf-8')
        tpl = Template(text).render(Context(params))
        return HttpResponse(tpl, content_type='application/pdf')
    except:

        template = 'template.html'
        return render(request, template, params)
