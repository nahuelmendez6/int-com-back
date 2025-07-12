# auth/urls

from django.urls import path
from .views import (RegisterUserAPIView,
                    UpdateUserAPIView)

urlpatterns = [
    path('register-user/', RegisterUserAPIView.as_view(), name='register'),
    path('update-user/', UpdateUserAPIView.as_view(), name='update-user'),
]