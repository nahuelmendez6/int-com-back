# Integración de Notificaciones en Tiempo Real - Frontend

## Descripción General

Este documento describe cómo integrar el sistema de notificaciones en tiempo real en el frontend. El sistema incluye:

- **API REST** para gestión de notificaciones
- **WebSockets** para notificaciones en tiempo real
- **Configuración personalizable** por usuario

## Endpoints de la API

### 1. Obtener Notificaciones
```
GET /notifications/
```
**Respuesta:**
```json
[
  {
    "id": 1,
    "title": "Nueva postulación recibida",
    "message": "Tu petición 'Reparación de techo' recibió una nueva postulación.",
    "notification_type": "postulation_created",
    "notification_type_display": "Nueva Postulación",
    "is_read": false,
    "created_at": "2024-01-15T10:30:00Z",
    "read_at": null,
    "related_postulation_id": 123,
    "related_petition_id": 456,
    "metadata": {
      "postulation_id": 123,
      "petition_id": 456,
      "provider_id": 789
    },
    "time_ago": "2 horas atrás"
  }
]
```

### 2. Estadísticas de Notificaciones
```
GET /notifications/stats/
```
**Respuesta:**
```json
{
  "total_notifications": 15,
  "unread_notifications": 3,
  "notifications_by_type": {
    "postulation_created": 5,
    "postulation_accepted": 2,
    "postulation_rejected": 1
  },
  "recent_notifications": [...]
}
```

### 3. Marcar como Leída
```
POST /notifications/{id}/mark-read/
```

### 4. Marcar Todas como Leídas
```
POST /notifications/mark-all-read/
```

### 5. Configuración de Notificaciones
```
GET /notifications/settings/
PUT /notifications/settings/
```

## WebSocket - Notificaciones en Tiempo Real

### Conexión
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/notifications/{user_id}/');
```

### Eventos Recibidos

#### 1. Conexión Establecida
```json
{
  "type": "connection_established",
  "unread_count": 3
}
```

#### 2. Nueva Notificación
```json
{
  "type": "notification_created",
  "notification": {
    "id": 1,
    "title": "Nueva postulación recibida",
    "message": "Tu petición 'Reparación de techo' recibió una nueva postulación.",
    "notification_type": "postulation_created",
    "is_read": false,
    "created_at": "2024-01-15T10:30:00Z",
    "time_ago": "Hace un momento"
  },
  "unread_count": 4
}
```

#### 3. Notificación Actualizada
```json
{
  "type": "notification_updated",
  "notification": {...},
  "unread_count": 3
}
```

#### 4. Notificación Eliminada
```json
{
  "type": "notification_deleted",
  "notification_id": 1,
  "unread_count": 2
}
```

### Envío de Comandos

#### Marcar como Leída
```javascript
ws.send(JSON.stringify({
  type: 'mark_as_read',
  notification_id: 1
}));
```

#### Obtener Conteo de No Leídas
```javascript
ws.send(JSON.stringify({
  type: 'get_unread_count'
}));
```

## Implementación en React/Vue/Angular

### Ejemplo con React

```jsx
import React, { useState, useEffect } from 'react';

const NotificationSystem = ({ userId }) => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    // Conectar WebSocket
    const websocket = new WebSocket(`ws://localhost:8000/ws/notifications/${userId}/`);
    
    websocket.onopen = () => {
      console.log('WebSocket conectado');
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'connection_established':
          setUnreadCount(data.unread_count);
          break;
        case 'notification_created':
          setNotifications(prev => [data.notification, ...prev]);
          setUnreadCount(data.unread_count);
          break;
        case 'notification_updated':
          setNotifications(prev => 
            prev.map(notif => 
              notif.id === data.notification.id ? data.notification : notif
            )
          );
          setUnreadCount(data.unread_count);
          break;
        case 'notification_deleted':
          setNotifications(prev => 
            prev.filter(notif => notif.id !== data.notification_id)
          );
          setUnreadCount(data.unread_count);
          break;
      }
    };

    websocket.onclose = () => {
      console.log('WebSocket desconectado');
      // Reconectar después de 3 segundos
      setTimeout(() => {
        setWs(new WebSocket(`ws://localhost:8000/ws/notifications/${userId}/`));
      }, 3000);
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, [userId]);

  const markAsRead = (notificationId) => {
    if (ws) {
      ws.send(JSON.stringify({
        type: 'mark_as_read',
        notification_id: notificationId
      }));
    }
  };

  return (
    <div>
      <h3>Notificaciones ({unreadCount} no leídas)</h3>
      {notifications.map(notification => (
        <div 
          key={notification.id}
          className={`notification ${!notification.is_read ? 'unread' : ''}`}
          onClick={() => markAsRead(notification.id)}
        >
          <h4>{notification.title}</h4>
          <p>{notification.message}</p>
          <small>{notification.time_ago}</small>
        </div>
      ))}
    </div>
  );
};

export default NotificationSystem;
```

### Ejemplo con Vue.js

```vue
<template>
  <div class="notification-system">
    <h3>Notificaciones ({{ unreadCount }} no leídas)</h3>
    <div 
      v-for="notification in notifications" 
      :key="notification.id"
      :class="['notification', { unread: !notification.is_read }]"
      @click="markAsRead(notification.id)"
    >
      <h4>{{ notification.title }}</h4>
      <p>{{ notification.message }}</p>
      <small>{{ notification.time_ago }}</small>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      notifications: [],
      unreadCount: 0,
      ws: null
    }
  },
  mounted() {
    this.connectWebSocket();
  },
  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
  },
  methods: {
    connectWebSocket() {
      this.ws = new WebSocket(`ws://localhost:8000/ws/notifications/${this.userId}/`);
      
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.handleWebSocketMessage(data);
      };
    },
    
    handleWebSocketMessage(data) {
      switch (data.type) {
        case 'connection_established':
          this.unreadCount = data.unread_count;
          break;
        case 'notification_created':
          this.notifications.unshift(data.notification);
          this.unreadCount = data.unread_count;
          break;
        // ... otros casos
      }
    },
    
    markAsRead(notificationId) {
      if (this.ws) {
        this.ws.send(JSON.stringify({
          type: 'mark_as_read',
          notification_id: notificationId
        }));
      }
    }
  }
}
</script>
```

## Tipos de Notificaciones

### 1. `postulation_created`
- **Cuándo:** Se crea una nueva postulación
- **Para:** Customer (dueño de la petición)
- **Acción:** Mostrar en tiempo real que alguien postuló

### 2. `postulation_state_changed`
- **Cuándo:** Cambia el estado de una postulación
- **Para:** Provider (quien postuló)
- **Acción:** Informar sobre el cambio de estado

### 3. `postulation_accepted`
- **Cuándo:** Una postulación es aceptada
- **Para:** Provider
- **Acción:** Celebrar la aceptación

### 4. `postulation_rejected`
- **Cuándo:** Una postulación es rechazada
- **Para:** Provider
- **Acción:** Informar sobre el rechazo

### 5. `petition_closed`
- **Cuándo:** Una petición se cierra
- **Para:** Customer y Providers que postularon
- **Acción:** Informar sobre el cierre

## Configuración de Usuario

Los usuarios pueden configurar qué tipos de notificaciones quieren recibir:

```javascript
// Obtener configuración actual
const settings = await fetch('/notifications/settings/').then(r => r.json());

// Actualizar configuración
await fetch('/notifications/settings/', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    postulation_created: true,
    postulation_state_changed: true,
    postulation_accepted: true,
    postulation_rejected: false,
    petition_closed: true,
    email_notifications: true,
    push_notifications: true
  })
});
```

## Consideraciones de Rendimiento

1. **Límite de notificaciones:** El sistema muestra las últimas 50 notificaciones por defecto
2. **Paginación:** Usar parámetros `?page=1&limit=20` en las consultas
3. **Caché:** Considerar cachear las notificaciones en el frontend
4. **Reconexión:** Implementar reconexión automática del WebSocket

## Seguridad

1. **Autenticación:** Todas las requests requieren JWT token
2. **Autorización:** Los usuarios solo ven sus propias notificaciones
3. **WebSocket:** Validación de usuario en la conexión
4. **Rate Limiting:** Implementar límites en la creación de notificaciones
