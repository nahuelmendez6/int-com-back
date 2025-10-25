from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

from .models import Notification, NotificationSettings
from .serializers import (
    NotificationSerializer, NotificationCreateSerializer, 
    NotificationUpdateSerializer, NotificationSettingsSerializer,
    NotificationStatsSerializer, NotificationTypeSerializer
)

class NotificationListCreateView(generics.ListCreateAPIView):
    """Lista y crea notificaciones"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NotificationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Obtiene, actualiza o elimina una notificación específica"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_stats(request):
    """Obtiene estadísticas de notificaciones del usuario"""
    user = request.user
    
    # Estadísticas básicas
    total_notifications = Notification.objects.filter(user=user).count()
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
    
    # Notificaciones por tipo
    notifications_by_type = {}
    for choice in Notification.objects.filter(user=user).values_list('notification_type', flat=True).distinct():
        count = Notification.objects.filter(user=user, notification_type=choice).count()
        notifications_by_type[choice] = count
    
    # Notificaciones recientes (últimas 5)
    recent_notifications = Notification.objects.filter(user=user)[:5]
    
    stats_data = {
        'total_notifications': total_notifications,
        'unread_notifications': unread_notifications,
        'notifications_by_type': notifications_by_type,
        'recent_notifications': recent_notifications
    }
    
    serializer = NotificationStatsSerializer(stats_data)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):
    """Marca todas las notificaciones del usuario como leídas"""
    user = request.user
    updated_count = Notification.objects.filter(user=user, is_read=False).update(
        is_read=True, 
        read_at=timezone.now()
    )
    
    return Response({
        'message': f'{updated_count} notificaciones marcadas como leídas',
        'updated_count': updated_count
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, notification_id):
    """Marca una notificación específica como leída"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.mark_as_read()
        return Response({'message': 'Notificación marcada como leída'})
    except Notification.DoesNotExist:
        return Response({'error': 'Notificación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notification_types(request):
    """Obtiene todos los tipos de notificación disponibles"""
    types = NotificationTypeSerializer.get_all_types()
    return Response(types)

class NotificationSettingsView(generics.RetrieveUpdateAPIView):
    """Obtiene y actualiza la configuración de notificaciones del usuario"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSettingsSerializer
    
    def get_object(self):
        settings, created = NotificationSettings.objects.get_or_create(
            user=self.request.user
        )
        return settings

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_count(request):
    """Obtiene el número de notificaciones no leídas"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return Response({'unread_count': count})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recent_notifications(request):
    """Obtiene las notificaciones recientes del usuario"""
    limit = request.GET.get('limit', 10)
    try:
        limit = int(limit)
    except ValueError:
        limit = 10
    
    notifications = Notification.objects.filter(user=request.user)[:limit]
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)
