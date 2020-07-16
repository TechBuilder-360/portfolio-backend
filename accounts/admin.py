from django.contrib import admin
from .models import User, Education, Skill, Social, \
    ProjectImage, Project, SocialLink, Experience, SubSkill

admin.site.register(User)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Social)
admin.site.register(SocialLink)
admin.site.register(ProjectImage)
admin.site.register(Project)
admin.site.register(SubSkill)
admin.site.register(Experience)
