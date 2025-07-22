from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TypeProviderViewSet, ProfessionViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'type-providers', TypeProviderViewSet)
router.register(r'professions', ProfessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
