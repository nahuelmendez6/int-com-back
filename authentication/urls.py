# auth/urls

from django.urls import path
from .views import (RegisterUserAPIView,
                    UpdateUserAPIView,
                    LoginAPIView)

urlpatterns = [
    path('register-user/', RegisterUserAPIView.as_view(), name='register'),

    path('login/', LoginAPIView.as_view(), name='login'),

    path('update-user/', UpdateUserAPIView.as_view(), name='update-user'),
]