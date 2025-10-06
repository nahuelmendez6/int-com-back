from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    TypeProviderViewSet,
    ProfessionViewSet,
    ProfileStatusAPIView,
    ProfileDetailAPIView,
    #CustomerProfileAPIView,
    #ProviderProfileAPIView,
    #ProviderProfileUpdateAPIView,
    #CustomerProfileUpdateAPIView,

    UserProfileAPIView,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'type-providers', TypeProviderViewSet)
router.register(r'professions', ProfessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile-status/', ProfileStatusAPIView.as_view()),
    path('profile/', ProfileDetailAPIView.as_view()),
    #path('customer-profile/', CustomerProfileAPIView.as_view()),
    #path('provider-profile/', ProviderProfileAPIView.as_view()),
    #path('provider-profile/update/', ProviderProfileUpdateAPIView.as_view()),
    #path('customer-profile/update/', CustomerProfileUpdateAPIView.as_view()),

    path('user/', UserProfileAPIView.as_view()),
]