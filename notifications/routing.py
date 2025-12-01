from django.urls import re_path
from . import consumers


# ====================================================
# Rutas de WebSocket para la app de notificaciones
# ====================================================
# Se define un patrón de URL que permitirá a los clientes conectarse
# al WebSocket de notificaciones en tiempo real.
# Cada usuario tiene un canal único identificado por su user_id.

"""
Define la URL que el frontend usará para conectarse vía WebSocket.
"""

websocket_urlpatterns = [
    re_path(r'ws/notifications/(?P<user_id>\w+)/$', consumers.NotificationConsumer.as_asgi()), # URL del WebSocket con parámetro user_id
                                                                                                 # Se instancia el consumer correspondiente
]
