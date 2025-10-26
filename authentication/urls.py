# auth/urls
# ====================================
# URLS DE AUTENTICACIÓN
# ====================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (RegisterUserAPIView,
                    UpdateUserAPIView,
                    LoginAPIView,
                    UserViewSet,
                    UserProfileUpdateView)


# ====================================
# ROUTER DE DRF
# ====================================
# Se crea un router para registrar automáticamente las rutas del ViewSet de usuarios
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')


# Esto generará rutas CRUD automáticas para UserViewSet:
# - /       → list, create
# - /<pk>/  → retrieve, update, destroy

# ====================================
# URLS PRINCIPALES DE LA APP DE AUTH
# ====================================

urlpatterns = [
    # Endpoint para registrar un nuevo usuario
    # Método: POST
    # URL: /register-user/
    path('register-user/', RegisterUserAPIView.as_view(), name='register'),


    # Endpoint para login de usuarios
    # Método: POST
    # URL: /login/
    path('login/', LoginAPIView.as_view(), name='login'),

    # Endpoint para actualizar información de usuario
    # Método: PUT/PATCH
    # URL: /update-user/
    path('update-user/', UpdateUserAPIView.as_view(), name='update-user'),

    #path('verify-code/', VerifyCodeAPIView.as_view(), name='verify-code'),
    # Endpoint para actualizar la foto de perfil del usuario
    # Método: PUT/PATCH
    # URL: /profile-picture/update/
    path('profile-picture/update/', UserProfileUpdateView.as_view(), name='profile-update'),

    # Incluir todas las rutas generadas automáticamente por el router
    path('', include(router.urls)),
]
