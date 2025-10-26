from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    TypeProviderViewSet,
    ProfessionViewSet,
    ProfileStatusAPIView,
    ProfileDetailAPIView,
    ProfileUserDetailAPIView,
    #CustomerProfileAPIView,
    #ProviderProfileAPIView,
    #ProviderProfileUpdateAPIView,
    #CustomerProfileUpdateAPIView,

    UserProfileAPIView,
)

# ====================================
# ROUTER DE DRF
# ====================================
# Se registran los ViewSets de catálogos para generar rutas CRUD automáticas
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'type-providers', TypeProviderViewSet)
router.register(r'professions', ProfessionViewSet)


# ====================================
# URLS PRINCIPALES DE LA APP PROFILES
# ====================================
urlpatterns = [
     # Incluir rutas automáticas generadas por los ViewSets del router
    path('', include(router.urls)),
    
    
    # Endpoint para verificar el estado del perfil del usuario actual
    # Método: GET
    # URL: /profile-status/
    path('profile-status/', ProfileStatusAPIView.as_view()),
    
    # Endpoint para obtener detalles del perfil del usuario logueado
    # Método: GET
    # URL: /profile/
    path('profile/', ProfileDetailAPIView.as_view()),
    
    # Endpoints específicos para listar catálogos (opcional, redundante con router)
    path('categories/', CategoryViewSet.as_view({'get': 'list'})),
    path('type-providers/', TypeProviderViewSet.as_view({'get': 'list'})),
    path('professions/', ProfessionViewSet.as_view({'get': 'list'})),
    
    # Endpoint para obtener detalles extendidos del usuario
    # Método: GET
    # URL: /user-detail/
    path('user-detail/', ProfileUserDetailAPIView.as_view()),

    # Endpoint para obtener/actualizar el perfil de usuario
    # Método: GET/PUT/PATCH según la implementación de UserProfileAPIView
    # URL: /user/
    path('user/', UserProfileAPIView.as_view()),
]