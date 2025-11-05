from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet

"""
Configuración de las rutas (URLs) para el módulo de conversaciones.

Este archivo utiliza un enrutador de Django REST Framework (DefaultRouter)
para registrar automáticamente las rutas relacionadas con el ViewSet
`ConversationViewSet`, que gestiona las operaciones sobre conversaciones
y mensajes entre usuarios.
"""

# Crear un enrutador por defecto de DRF, que genera automáticamente las rutas CRUD
router = DefaultRouter()

# Registrar el ViewSet de conversaciones en el enrutador
# basename='conversation' define el nombre base para las rutas generadas:
#   - /conversations/ → lista y creación
#   - /conversations/{id}/ → detalle
#   - /conversations/start/ → acción personalizada (iniciar conversación)
#   - /conversations/{id}/send/ → acción personalizada (enviar mensaje)
#   - /conversations/{id}/mark_as_read/ → acción personalizada (marcar mensajes leídos)
router.register('conversations', ConversationViewSet, basename='conversation')

# Generar automáticamente la lista de URLs a partir del router

urlpatterns = router.urls
