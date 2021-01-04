from django.urls import path
from .views import resume_download

urlpatterns = [
    path('download/<username>/', resume_download, name="resume-download")
]