from django.contrib import admin
from .models import User, Contact, Template


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email',)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'submitted_by', 'creation_date',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "created_on")


admin.site.register(User, UserAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Contact, ContactAdmin)
