# app: notifications/models.py

from django.db import models
from django.utils import timezone

from django.conf import settings

class NotificationType(models.TextChoices):
    POSTULATION_CREATED = 'postulation_created', 'Nueva Postulación'
    POSTULATION_STATE_CHANGED = 'postulation_state_changed', 'Estado de Postulación Cambiado'
    POSTULATION_ACCEPTED = 'postulation_accepted', 'Postulación Aceptada'
    POSTULATION_REJECTED = 'postulation_rejected', 'Postulación Rechazada'
    PETITION_CLOSED = 'petition_closed', 'Petición Cerrada'
    GENERAL = 'general', 'General'

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.CASCADE, 
                             related_name='notifications',
                             db_column='id_user')
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    notification_type = models.CharField(
        max_length=50, 
        choices=NotificationType.choices, 
        default=NotificationType.GENERAL
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Campos para relacionar con otros modelos
    related_postulation_id = models.IntegerField(null=True, blank=True)
    related_petition_id = models.IntegerField(null=True, blank=True)
    
    # Metadata adicional
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'n_notification'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def mark_as_read(self):
        """Marca la notificación como leída"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    def __str__(self):
        return f"{self.title} → {self.user.username}"

class NotificationSettings(models.Model):
    """Configuración de notificaciones por usuario"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        db_column='id_user', 
        related_name='notification_settings',
        )
    
    # Configuraciones por tipo de notificación
    postulation_created = models.BooleanField(default=True)
    postulation_state_changed = models.BooleanField(default=True)
    postulation_accepted = models.BooleanField(default=True)
    postulation_rejected = models.BooleanField(default=True)
    petition_closed = models.BooleanField(default=True)
    
    # Configuraciones generales
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'n_notification_settings'

    def __str__(self):
        return f"Settings for {self.user.username}"
