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

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'type-providers', TypeProviderViewSet)
router.register(r'professions', ProfessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile-status/', ProfileStatusAPIView.as_view()),
    path('profile/', ProfileDetailAPIView.as_view()),
    path('categories/', CategoryViewSet.as_view({'get': 'list'})),
    path('type-providers/', TypeProviderViewSet.as_view({'get': 'list'})),
    path('professions/', ProfessionViewSet.as_view({'get': 'list'})),
    path('user-detail/', ProfileUserDetailAPIView.as_view()),

    path('user/', UserProfileAPIView.as_view()),
]