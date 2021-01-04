from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('resume/', include('resume.urls')),
    path('', TemplateView.as_view(template_name="index.html")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
    path('api/doc/', TemplateView.as_view(template_name="doc.html"), name="doc"),
    path('', include('social_django.urls', namespace='social')),
]
