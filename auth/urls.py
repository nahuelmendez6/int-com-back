# auth/urls

from django.urls import path
from .views import RegisterUserAPIView

urrlpatterns = [
    path('register-user/', RegisterUserAPIView.as_view(), name='register')
]