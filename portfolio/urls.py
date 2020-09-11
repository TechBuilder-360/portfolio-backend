from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as login_views
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('accounts.urls')),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
    path('', TemplateView.as_view(template_name="index.html")),
    # path('', include('social_django.urls', namespace='social')),
    # path('logout/', login_views.LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
