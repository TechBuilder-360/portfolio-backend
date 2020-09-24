from django.urls import path
from .views import googleAuth

urlpatterns = [
    path('google/auth/', googleAuth, name='google_login'),
]