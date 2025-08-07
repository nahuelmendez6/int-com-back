from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    TypeProviderViewSet,
    ProfessionViewSet,
    ProfileStatusAPIView,
    ProfileDetailAPIView,
    ProviderProfileAPIView,
    ProviderProfileUpdateAPIView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'type-providers', TypeProviderViewSet)
router.register(r'professions', ProfessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile-status/', ProfileStatusAPIView.as_view()),
    path('profile/', ProfileDetailAPIView.as_view()),
    path('provider-profile/', ProviderProfileAPIView.as_view()),
    path('provider-profile/update/', ProviderProfileUpdateAPIView.as_view()),
]