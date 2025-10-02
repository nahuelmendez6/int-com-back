from django.urls import path
from .views import AvaialabilityAPIView

urlpatterns = [

    # Crear disponibilidad
    path('add/', AvaialabilityAPIView.as_view(), name='availability-create'),

    # Listar disponibilidad por proveedor
    path('provider/<int:id_provider>/', AvaialabilityAPIView.as_view(), name='availability-by-provider'),

    # Operar sobre una disponibilidad concreta
    path("edit/<int:pk>/", AvaialabilityAPIView.as_view(), name="availability-detail"),

]