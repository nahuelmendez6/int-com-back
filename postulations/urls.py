from django.urls import path
from .views import PostulationAPIView, PostulationMaterialAPIView, PostulationStatisticsAPIView

urlpatterns = [
    # Listado de todas las postulaciones del proveedor
    # o detalle por id_postulation
    path('', PostulationAPIView.as_view(), name='postulation-list'),

    # Detalle, actualización (PATCH) y eventualmente DELETE de una postulación
    path('<int:pk>/', PostulationAPIView.as_view(), name='postulation-detail'),

    # Listado de postulaciones de una petición específica (para clientes)
    path('by-petition/<int:id_petition>/', PostulationAPIView.as_view(), name='postulation-by-petition'),
    
    # Estadísticas de postulaciones para proveedores
    path('statistics/', PostulationStatisticsAPIView.as_view(), name='postulation-statistics'),
    
    path('materials/', PostulationMaterialAPIView.as_view(), name='postulation_material_create'),
    path('materials/<int:id_postulation>/', PostulationMaterialAPIView.as_view(), name='postulation_material_list'),
    path('materials/item/<int:pk>/', PostulationMaterialAPIView.as_view(), name='postulation_material_detail'),
]
