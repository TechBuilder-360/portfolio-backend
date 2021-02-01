from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import Login, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', Login, name="login"),
    path('logout/', logout_view, name="logout"),
    path('resume/', include('resume.urls')),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
    path('api/doc/', TemplateView.as_view(template_name="doc.html"), name="doc"),
    path('', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
