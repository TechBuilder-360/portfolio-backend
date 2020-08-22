from django.contrib import admin
from django.conf import  settings
from django.urls import path, include
from django.contrib.auth import views as login_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),
    path('', TemplateView.as_view(template_name="accounts/google_auth.html")),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', login_views.LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
