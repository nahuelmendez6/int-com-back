# auth/urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (RegisterUserAPIView,
                    UpdateUserAPIView,
                    LoginAPIView,
                    VerifyCodeAPIView,
                    UserViewSet,
                    UpdateProviderAPIView)

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('register-user/', RegisterUserAPIView.as_view(), name='register'),

    path('login/', LoginAPIView.as_view(), name='login'),

    path('update-user/', UpdateUserAPIView.as_view(), name='update-user'),

    path('update-provider/', UpdateProviderAPIView.as_view(), name='update-provider'),

    path('verify-code/', VerifyCodeAPIView.as_view(), name='verify-code'),

    path('', include(router.urls)),
]