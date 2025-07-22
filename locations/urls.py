from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, ProvinceViewSet, DepartmentViewSet, CityViewSet, AddressViewSet, ProviderCityViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'provinces', ProvinceViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'cities', CityViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'provider-cities', ProviderCityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]