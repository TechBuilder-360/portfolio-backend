from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Education, Skill, Social, \
    ProjectImage, Project, SocialLink, Experience, SubSkill

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

class SocialLinkInline(admin.TabularInline):
    model = Project
    extra = 1


class UserAdmin(BaseUserAdmin):
    inlines = (ProjectInline, ExperienceInline, EducationInline, SkillInline, SocialLinkInline)



admin.site.register(User, UserAdmin)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Social)
admin.site.register(SocialLink)
admin.site.register(ProjectImage)
admin.site.register(Project)
admin.site.register(SubSkill)
admin.site.register(Experience)
