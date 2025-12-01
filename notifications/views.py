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


# -----------------------------------------------------------
# LISTADO Y CREACIÓN DE NOTIFICACIONES
# -----------------------------------------------------------

class NotificationListCreateView(generics.ListCreateAPIView):
    """Lista y crea notificaciones"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtra solo las notificaciones del usuario autenticado
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        # Usa un serializer distinto al crear (POST)
        if self.request.method == 'POST':
            return NotificationCreateSerializer
        
        # Usa el serializer estándar para listar
        return NotificationSerializer
    
    def perform_create(self, serializer):
        # Al crear, asigna automáticamente la notificación al usuario
        serializer.save(user=self.request.user)


# -----------------------------------------------------------
# OBTENER, ACTUALIZAR O ELIMINAR UNA NOTIFICACIÓN ESPECÍFICA
# -----------------------------------------------------------

class NotificationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Obtiene, actualiza o elimina una notificación específica"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        # Asegura que solo acceda a sus propias notificaciones
        return Notification.objects.filter(user=self.request.user)


# -----------------------------------------------------------
# ESTADÍSTICAS DE NOTIFICACIONES
# -----------------------------------------------------------


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_stats(request):
    """Obtiene estadísticas de notificaciones del usuario"""
    user = request.user
    
    # Cantidad total de notificaciones
    total_notifications = Notification.objects.filter(user=user).count()
    
    # Cantidad de no leídas
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
    
    # Agrupación por tipo con COUNT
    notifications_by_type = {
        item['notification_type']: item['total']
        for item in Notification.objects.filter(user=user)
        .values('notification_type')
        .annotate(total=Count('id'))
    }
    
    # Notificaciones recientes (últimas 5)
    recent_notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Estructura final enviada al serializer
    stats_data = {
        'total_notifications': total_notifications,
        'unread_notifications': unread_notifications,
        'notifications_by_type': notifications_by_type,
        'recent_notifications': recent_notifications
    }
    
    serializer = NotificationStatsSerializer(stats_data)
    return Response(serializer.data)

# -----------------------------------------------------------
# MARCAR TODAS LAS NOTIFICACIONES COMO LEÍDAS
# -----------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):
    """Marca todas las notificaciones del usuario como leídas"""
    user = request.user

    # Actualiza en bloque todas las no leídas
    updated_count = Notification.objects.filter(user=user, is_read=False).update(
        is_read=True, 
        read_at=timezone.now()
    )
    
    return Response({
        'message': f'{updated_count} notificaciones marcadas como leídas',
        'updated_count': updated_count
    })


# -----------------------------------------------------------
# MARCAR UNA NOTIFICACIÓN COMO LEÍDA
# -----------------------------------------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, notification_id):
    """Marca una notificación específica como leída"""
    try:
        # Verifica propiedad de la notificación
        notification = Notification.objects.get(id=notification_id, user=request.user)
        
        # Usa un método del modelo para marcarla como leída
        notification.mark_as_read()
        return Response({'message': 'Notificación marcada como leída'})
    except Notification.DoesNotExist:
        return Response({'error': 'Notificación no encontrada'}, status=status.HTTP_404_NOT_FOUND)


# -----------------------------------------------------------
# OBTENER TODOS LOS TIPOS DE NOTIFICACIÓN DISPONIBLES
# -----------------------------------------------------------
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
