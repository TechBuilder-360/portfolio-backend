from django.contrib import admin
from .models import User, Contact


class UserAdmin(admin.ModelAdmin):

    list_display = ('username', 'first_name', 'last_name', 'email', )


admin.site.register(User, UserAdmin)
admin.site.register(Contact)
