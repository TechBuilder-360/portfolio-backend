from django.contrib import admin
from .models import Education, Skill, Project, SocialLink, Experience, SubSkill

admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(SocialLink)
admin.site.register(Project)
admin.site.register(SubSkill)
admin.site.register(Experience)
