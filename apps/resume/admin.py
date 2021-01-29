from django.contrib import admin
from .models import Education, Skill, Project, SocialLink, Experience, SubSkill, Accomplishment


class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'institution', 'course', 'degree',)


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'position',)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')


class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'url')


class SubSkillAdmin(admin.ModelAdmin):
    list_display = ('skill', 'title')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'project_url', 'title')


class AccomplishmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'issuer', 'course')


admin.site.register(Education, EducationAdmin)
admin.site.register(Accomplishment, AccomplishmentAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(SubSkill, SubSkillAdmin)
admin.site.register(Experience, ExperienceAdmin)
