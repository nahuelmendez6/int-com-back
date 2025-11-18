import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer para notificaciones en tiempo real.

    Funcionalidad:
    - Conectar un usuario al canal de notificaciones.
    - Enviar notificaciones nuevas, actualizadas o eliminadas.
    - Marcar notificaciones como leídas.
    - Consultar número de notificaciones no leídas.
    """
    async def connect(self):
        """
        Conecta al WebSocket y se une al grupo correspondiente al usuario.
        Envía la cantidad de notificaciones no leídas al conectar.
        """
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_name = f'notifications_{self.user_id}'
        
        # Verificar que el usuario existe
        user = await self.get_user(self.user_id)
        if not user:
            await self.close()
            return
        
        # Unirse al grupo
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Enviar notificaciones no leídas al conectar
        unread_count = await self.get_unread_count(self.user_id)
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'unread_count': unread_count
        }))

    async def disconnect(self, close_code):
        """
        Desconecta del WebSocket y sale del grupo del usuario.
        """
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Recibe mensajes desde el WebSocket.

        Tipos de mensajes soportados:
        - mark_as_read: marca una notificación específica como leída.
        - get_unread_count: solicita el número de notificaciones no leídas.
        """
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'mark_as_read':
                notification_id = text_data_json.get('notification_id')
                await self.mark_notification_as_read(notification_id)
                
            elif message_type == 'get_unread_count':
                count = await self.get_unread_count(self.user_id)
                await self.send(text_data=json.dumps({
                    'type': 'unread_count',
                    'count': count
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))
    # ====================================================
    # Métodos para enviar notificaciones desde el backend
    # ====================================================
    async def notification_created(self, event):
        """
        Envía al cliente una notificación recién creada.
        """
        print(f"📡 CONSUMER: Recibido evento 'notification_created' para el grupo '{self.user_group_name}'. Enviando al cliente.")
        await self.send(text_data=json.dumps({
            'type': 'notification_created',
            'notification': event['notification'],
            'unread_count': event['unread_count']
        }))

    async def notification_updated(self, event):
        """Envía una notificación actualizada al cliente"""
        await self.send(text_data=json.dumps({
            'type': 'notification_updated',
            'notification': event['notification'],
            'unread_count': event['unread_count']
        }))

    async def notification_deleted(self, event):
        """
        Envía información sobre una notificación eliminada.
        """
        await self.send(text_data=json.dumps({
            'type': 'notification_deleted',
            'notification_id': event['notification_id'],
            'unread_count': event['unread_count']
        }))
    # ====================================================
    # Métodos auxiliares sincronizados a la base de datos
    # ====================================================
    @database_sync_to_async
    def get_user(self, user_id):
        """
        Obtiene un usuario por ID.
        Devuelve None si no existe.
        """
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    """
    def get_user(self, user_id):
        try:
            User = get_user_model()
            return User.objects.get(id_user=user_id)
        except User.DoesNotExist:
            return None
    """
            
    @database_sync_to_async
    def get_unread_count(self, user_id):
        """Obtiene el número de notificaciones no leídas"""
        from .models import Notification
        return Notification.objects.filter(user_id=user_id, is_read=False).count()

    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        """Marca una notificación como leída"""
        from .models import Notification
        try:
            notification = Notification.objects.get(
                id=notification_id, 
                user_id=self.user_id
            )
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False
