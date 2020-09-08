from django.urls import path
from .views import index, dashboard, userLogin

urlpatterns = [
    path('', index, name="google"),
    path('login/', userLogin, name='login'),
    path('success/', dashboard, name='dashboard')
]