from .views import avartar
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('upload/', csrf_exempt(avartar), name="upload")
]