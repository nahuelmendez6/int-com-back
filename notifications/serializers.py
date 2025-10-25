from rest_framework import serializers
from .models import Notification, NotificationSettings, NotificationType

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para notificaciones"""
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'notification_type', 'notification_type_display',
            'is_read', 'created_at', 'read_at', 'related_postulation_id', 
            'related_petition_id', 'metadata', 'time_ago'
        ]
        read_only_fields = ['id', 'created_at', 'read_at', 'time_ago']

    def get_time_ago(self, obj):
        """Calcula el tiempo transcurrido desde la creación"""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 0:
            return f"{diff.days} día{'s' if diff.days > 1 else ''} atrás"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hora{'s' if hours > 1 else ''} atrás"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minuto{'s' if minutes > 1 else ''} atrás"
        else:
            return "Hace un momento"

class NotificationCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear notificaciones"""
    
    class Meta:
        model = Notification
        fields = ['user', 'title', 'message', 'notification_type', 'related_postulation_id', 'related_petition_id', 'metadata']

class NotificationUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar notificaciones (marcar como leída)"""
    
    class Meta:
        model = Notification
        fields = ['is_read']

class NotificationSettingsSerializer(serializers.ModelSerializer):
    """Serializer para configuración de notificaciones"""
    
    class Meta:
        model = NotificationSettings
        fields = [
            'postulation_created', 'postulation_state_changed', 
            'postulation_accepted', 'postulation_rejected', 
            'petition_closed', 'email_notifications', 'push_notifications'
        ]

class NotificationStatsSerializer(serializers.Serializer):
    """Serializer para estadísticas de notificaciones"""
    total_notifications = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()
    notifications_by_type = serializers.DictField()
    recent_notifications = NotificationSerializer(many=True)

class NotificationTypeSerializer(serializers.Serializer):
    """Serializer para tipos de notificación"""
    value = serializers.CharField()
    label = serializers.CharField()
    
    @classmethod
    def get_all_types(cls):
        """Retorna todos los tipos de notificación disponibles"""
        return [
            {'value': choice[0], 'label': choice[1]} 
            for choice in NotificationType.choices
        ]
