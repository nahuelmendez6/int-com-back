from django.urls import path

from .views import AddressAPIView

urlpatterns = [
    path('update-address/', AddressAPIView.as_view(), name='update-address'),
]

