from django.urls import path
from .views import PostulationAPIView

urlpatterns = [
    # Listado de todas las postulaciones del proveedor
    # o detalle por id_postulation
    path('postulations/', PostulationAPIView.as_view(), name='postulation-list'),

    # Detalle, actualización (PATCH) y eventualmente DELETE de una postulación
    path('postulations/<int:pk>/', PostulationAPIView.as_view(), name='postulation-detail'),

    # Listado de postulaciones de una petición específica (para clientes)
    path('postulations/by-petition/<int:id_petition>/', PostulationAPIView.as_view(), name='postulation-by-petition'),
]
