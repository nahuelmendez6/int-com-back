# Sistema de Notificaciones en Tiempo Real

## Descripción

Sistema completo de notificaciones en tiempo real para la plataforma de integración comunitaria. Incluye notificaciones automáticas para postulaciones, cambios de estado, y eventos del sistema.

## Características

- ✅ **Notificaciones en tiempo real** via WebSockets
- ✅ **API REST completa** para gestión de notificaciones
- ✅ **Configuración personalizable** por usuario
- ✅ **Notificaciones automáticas** para eventos del sistema
- ✅ **Tipos de notificación** específicos (postulaciones, peticiones, etc.)
- ✅ **Estadísticas y métricas** de notificaciones
- ✅ **Admin interface** para gestión
- ✅ **Documentación completa** para integración frontend

## Estructura del Sistema

### Modelos
- `Notification`: Notificaciones del usuario
- `NotificationSettings`: Configuración personalizada por usuario
- `NotificationType`: Tipos de notificación disponibles

### API Endpoints
- `GET /notifications/` - Listar notificaciones
- `POST /notifications/` - Crear notificación
- `GET /notifications/stats/` - Estadísticas
- `POST /notifications/mark-all-read/` - Marcar todas como leídas
- `GET /notifications/settings/` - Configuración del usuario
- `PUT /notifications/settings/` - Actualizar configuración

### WebSocket
- `ws://localhost:8000/ws/notifications/{user_id}/` - Conexión en tiempo real

### Signals Automáticos
- **Postulaciones**: Notificación al customer cuando se crea una postulación
- **Cambios de estado**: Notificación al provider cuando cambia el estado
- **Peticiones**: Notificación a providers cuando se crea una petición
- **Cierre de peticiones**: Notificación a todos los involucrados

## Instalación y Configuración

### 1. Dependencias Requeridas
```bash
pip install channels channels-redis redis
```

### 2. Configuración en settings.py
```python
INSTALLED_APPS = [
    # ... otras apps
    'channels',
    'notifications',
]

ASGI_APPLICATION = "integracion_comunitaria.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

### 3. Migraciones
```bash
python manage.py makemigrations notifications
python manage.py migrate
```

### 4. Iniciar Redis
```bash
redis-server
```

### 5. Iniciar el servidor
```bash
python manage.py runserver
```

## Uso del Sistema

### Crear Notificación Manual
```python
from notifications.services import notification_service

notification_service.send_notification(
    user_id=123,
    title="Nueva notificación",
    message="Este es un mensaje de prueba",
    notification_type='general',
    metadata={'custom_data': 'value'}
)
```

### Enviar a Múltiples Usuarios
```python
notification_service.send_bulk_notification(
    user_ids=[123, 456, 789],
    title="Anuncio importante",
    message="Mantenimiento programado",
    notification_type='general'
)
```

### WebSocket en Frontend
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/notifications/123/');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Nueva notificación:', data);
};
```

## Tipos de Notificación

| Tipo | Descripción | Cuándo se activa |
|------|-------------|------------------|
| `postulation_created` | Nueva postulación | Cuando se crea una postulación |
| `postulation_state_changed` | Estado cambiado | Cuando cambia el estado de una postulación |
| `postulation_accepted` | Postulación aceptada | Cuando se acepta una postulación |
| `postulation_rejected` | Postulación rechazada | Cuando se rechaza una postulación |
| `petition_closed` | Petición cerrada | Cuando se cierra una petición |
| `general` | General | Notificaciones del sistema |

## Configuración de Usuario

Los usuarios pueden configurar qué notificaciones recibir:

```python
# Obtener configuración
settings = NotificationSettings.objects.get(user=user)

# Actualizar configuración
settings.postulation_created = True
settings.email_notifications = False
settings.save()
```

## Eventos WebSocket

### Recibidos del Servidor
- `connection_established`: Conexión establecida
- `notification_created`: Nueva notificación
- `notification_updated`: Notificación actualizada
- `notification_deleted`: Notificación eliminada

### Enviados al Servidor
- `mark_as_read`: Marcar como leída
- `get_unread_count`: Obtener conteo de no leídas

## Monitoreo y Debugging

### Logs de Notificaciones
```python
import logging
logger = logging.getLogger('notifications')

# En el servicio
logger.info(f"Notificación enviada a usuario {user_id}: {title}")
```

### Admin Interface
- Acceso: `/admin/notifications/`
- Gestión de notificaciones
- Configuración de usuarios
- Estadísticas del sistema

## Consideraciones de Rendimiento

1. **Índices de base de datos** optimizados para consultas frecuentes
2. **Paginación** en listados de notificaciones
3. **Límites** en el número de notificaciones por usuario
4. **Cache** para estadísticas frecuentes
5. **WebSocket** con reconexión automática

## Seguridad

1. **Autenticación JWT** requerida para todas las requests
2. **Autorización** por usuario (solo sus notificaciones)
3. **Validación** de datos en WebSocket
4. **Rate limiting** para prevenir spam

## Próximos Pasos

- [ ] Implementar notificaciones por email
- [ ] Agregar notificaciones push para móviles
- [ ] Implementar templates de notificación
- [ ] Agregar métricas avanzadas
- [ ] Implementar notificaciones programadas
- [ ] Agregar notificaciones por categorías

## Soporte

Para dudas o problemas, revisar:
1. Logs del servidor Django
2. Logs de Redis
3. Console del navegador (WebSocket)
4. Documentación de Channels
5. Archivo `FRONTEND_INTEGRATION.md`
