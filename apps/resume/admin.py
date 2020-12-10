from django.contrib import admin
from .models import Education, Skill, Project, SocialLink, Experience, SubSkill


class EducationAdmin(admin.ModelAdmin):

    list_display = ('user', 'institution', 'course', 'degree', )


class ExperienceAdmin(admin.ModelAdmin):

    list_display = ('user', 'organization', 'position', )


admin.site.register(Education, EducationAdmin)
admin.site.register(Skill)
admin.site.register(SocialLink)
admin.site.register(Project)
admin.site.register(SubSkill)
admin.site.register(Experience, ExperienceAdmin)
