from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import Login, logout_view
from accounts.api import UserDetailViewSet

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', Login, name="login"),
    path('logout/', logout_view, name="logout"),
    path('resume/', include('resume.urls')),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
    path('', include('social_django.urls', namespace='social')),
    path('api/user-detail/<int:id>', UserDetailViewSet.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
