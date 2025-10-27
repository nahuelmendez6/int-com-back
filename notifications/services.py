import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

from .models import Notification, NotificationSettings
from .serializers import NotificationSerializer



# ====================================================
# Servicio de Notificaciones
# ====================================================
class NotificationService:
    """Servicio para manejar notificaciones en tiempo real"""
    
    def __init__(self):
        self.channel_layer = get_channel_layer()
    
    # ====================================================
    # Envío de notificación individual
    # ====================================================
    def send_notification(self, user_id, title, message, notification_type='general', 
                         related_postulation_id=None, related_petition_id=None, metadata=None):
        """
        Envía una notificación a un usuario específico.

        - Verifica si el usuario existe.
        - Respeta la configuración de notificaciones del usuario.
        - Crea la notificación en la base de datos.
        - Envía por WebSocket si el usuario tiene habilitado push_notifications.
        """
        try:
            User = get_user_model()
            user = User.objects.get(id_user=user_id)
            
            # Verificar configuración de notificaciones del usuario
            settings, created = NotificationSettings.objects.get_or_create(user=user)
            
            # Verificar si el usuario tiene habilitado este tipo de notificación
            if not self._is_notification_enabled(settings, notification_type):
                return None
            
            # Crear la notificación
            notification = Notification.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                related_postulation_id=related_postulation_id,
                related_petition_id=related_petition_id,
                metadata=metadata or {}
            )
            
            # Enviar por WebSocket si está habilitado
            if settings.push_notifications:
                self._send_websocket_notification(user_id, notification)
            
            return notification
            
        except get_user_model().DoesNotExist:
            return None
    
    # ====================================================
    # Envío de notificaciones masivas
    # ====================================================
    def send_bulk_notification(self, user_ids, title, message, notification_type='general', 
                              related_postulation_id=None, related_petition_id=None, metadata=None):
        """
        Envía la misma notificación a múltiples usuarios.

        Retorna la lista de notificaciones creadas.
        """
        notifications = []
        for user_id in user_ids:
            notification = self.send_notification(
                user_id, title, message, notification_type,
                related_postulation_id, related_petition_id, metadata
            )
            if notification:
                notifications.append(notification)
        return notifications
    
    # ====================================================
    # Validación de configuración de notificaciones
    # ====================================================
    def _is_notification_enabled(self, settings, notification_type):
        """
        Comprueba si un tipo de notificación está habilitado para el usuario
        según sus preferencias en NotificationSettings.
        """
        type_mapping = {
            'postulation_created': settings.postulation_created,
            'postulation_state_changed': settings.postulation_state_changed,
            'postulation_accepted': settings.postulation_accepted,
            'postulation_rejected': settings.postulation_rejected,
            'petition_closed': settings.petition_closed,
        }
        return type_mapping.get(notification_type, True)
    
    # ====================================================
    # Envío de notificación por WebSocket
    # ====================================================
    def _send_websocket_notification(self, user_id, notification):
        """
        Envía la notificación en tiempo real al grupo del usuario
        usando Channels y WebSocket.
        """
        if not self.channel_layer:
            return
        
        # Serializar la notificación
        serializer = NotificationSerializer(notification)
        notification_data = serializer.data
        
        # Obtener conteo de no leídas
        unread_count = Notification.objects.filter(user_id=user_id, is_read=False).count()
        
        # Enviar al grupo del usuario
        async_to_sync(self.channel_layer.group_send)(
            f'notifications_{user_id}',
            {
                'type': 'notification_created',
                'notification': notification_data,
                'unread_count': unread_count
            }
        )
    
    # ====================================================
    # Marcar notificación como leída
    # ====================================================
    def mark_notification_as_read(self, notification_id, user_id):
        """
        Marca una notificación como leída.

        - Actualiza el campo is_read y read_at en DB.
        - Envía la actualización al cliente por WebSocket.
        """
        try:
            notification = Notification.objects.get(id=notification_id, user_id=user_id)
            notification.mark_as_read()
            
            # Notificar por WebSocket
            if self.channel_layer:
                serializer = NotificationSerializer(notification)
                unread_count = Notification.objects.filter(user_id=user_id, is_read=False).count()
                
                async_to_sync(self.channel_layer.group_send)(
                    f'notifications_{user_id}',
                    {
                        'type': 'notification_updated',
                        'notification': serializer.data,
                        'unread_count': unread_count
                    }
                )
            
            return True
        except Notification.DoesNotExist:
            return False
    
    # ====================================================
    # Eliminar notificación
    # ====================================================
    def delete_notification(self, notification_id, user_id):
        """
        Elimina una notificación de la base de datos.

        - Notifica al cliente por WebSocket sobre la eliminación.
        """
        try:
            notification = Notification.objects.get(id=notification_id, user_id=user_id)
            notification.delete()
            
            # Notificar por WebSocket
            if self.channel_layer:
                unread_count = Notification.objects.filter(user_id=user_id, is_read=False).count()
                
                async_to_sync(self.channel_layer.group_send)(
                    f'notifications_{user_id}',
                    {
                        'type': 'notification_deleted',
                        'notification_id': notification_id,
                        'unread_count': unread_count
                    }
                )
            
            return True
        except Notification.DoesNotExist:
            return False
# ====================================================
# Instancia global del servicio de notificaciones
# ====================================================
notification_service = NotificationService()
