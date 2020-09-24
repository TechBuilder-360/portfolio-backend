from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
    path('', TemplateView.as_view(template_name="index.html")),
    path('google/', TemplateView.as_view(template_name="accounts/google_auth.html")),
    path('api/', include('accounts.urls')),
    path('', include('social_django.urls', namespace='social')),
]
