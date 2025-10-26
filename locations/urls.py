from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CountryViewSet,
                    ProvinceViewSet,
                    DepartmentViewSet,
                    CityViewSet,
                    AddressViewSet,
                    ProviderCityViewSet,
                    ProviderCitiesAPIView, ProviderCityDeleteAPIView)


# ====================================
# ROUTER PRINCIPAL
# ====================================
router = DefaultRouter()

# Registramos los ViewSets de los modelos principales con rutas RESTful automáticas
router.register(r'countries', CountryViewSet)
router.register(r'provinces', ProvinceViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'cities', CityViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'provider-cities', ProviderCityViewSet)

urlpatterns = [
    # Incluye todas las rutas del router
    path('', include(router.urls)),
    
    # Obtener todas las ciudades donde un proveedor está asignado
    # GET /cities-area/<provider_id>/
    path('cities-area/<int:provider_id>/', ProviderCitiesAPIView.as_view(), name='cities-area'),
    
    # Eliminar una relación proveedor-ciudad específica
    # DELETE /providers/<provider_id>/cities/<city_id>/
    path('providers/<int:provider_id>/cities/<int:city_id>/', ProviderCityDeleteAPIView.as_view(), name='providercity-delete'),
]