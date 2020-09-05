from django.urls import path
from .views import index, dashboard

urlpatterns = [
    path('', index, name="google"),
    path('success/', dashboard, name='dashboard')
]