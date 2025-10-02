from django.urls import path
from .views import AvaialabilityAPIView

urlpatterns = [

    # Crear disponibilidad
    path('availabilities/', AvaialabilityAPIView.as_view(), name='availability-create'),

    # Listar disponibilidad por proveedor
    path('availabilities/provider/<int:id_provider>/', AvaialabilityAPIView.as_view(), name='availability-by-provider'),

    # Operar sobre una disponibilidad concreta
    path("availabilities/<int:pk>/", AvaialabilityAPIView.as_view(), name="availability-detail"),

]