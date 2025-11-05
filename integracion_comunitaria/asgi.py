"""
Configuración ASGI para el proyecto **integracion_comunitaria**.

Este archivo expone la aplicación ASGI como una variable de módulo llamada ``application``,
que permite a Django manejar solicitudes tanto HTTP como WebSocket.

La configuración combina:
- `get_asgi_application()` para manejar peticiones HTTP tradicionales.
- `ProtocolTypeRouter` para enrutar distintos tipos de conexiones.
- `AuthMiddlewareStack` y `URLRouter` de Channels para gestionar conexiones WebSocket autenticadas.

Más información:
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import notifications.routing

# Establece el módulo de configuración predeterminado de Django para ASGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integracion_comunitaria.settings')

# Define la aplicación ASGI principal
# Usa ProtocolTypeRouter para manejar distintos tipos de protocolos:
# - "http": Manejado por la aplicación ASGI estándar de Django.
# - "websocket": Manejado por Channels con soporte para autenticación y rutas.
application = ProtocolTypeRouter({

    # Maneja las solicitudes HTTP regulares (Django tradicional)
    "http": get_asgi_application(),

    # Maneja las conexiones WebSocket
    "websocket": AuthMiddlewareStack(

        # URLRouter se encarga de enrutar las conexiones WebSocket
        # a los consumidores definidos en notifications.routing
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    ),
})
