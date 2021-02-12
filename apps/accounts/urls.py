from .views import avartar, dashboard, download
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('upload/', csrf_exempt(avartar), name="upload"),
    path('me/', dashboard, name="dashboard"),
    path('me/edit/<int:pk>', dashboard, name="template_edit"),
    path('download/', download, name="download"),
]
