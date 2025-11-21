from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from notifications.models import Notification
from notifications.services import notification_service
from .models import Postulation
from petitions.models import Petition
from authentication.models import Customer, Provider



# ====================================================
# SIGNAL: notify_on_postulation_create
# ====================================================
@receiver(post_save, sender=Postulation)
def notify_on_postulation_create(sender, instance, created, **kwargs):
    """
    Señal que se ejecuta automáticamente cuando se crea una nueva postulación.
    Objetivo:
        → Notificar al cliente (Customer) propietario de la petición correspondiente.
    Flujo:
        1. Se detecta una nueva instancia de Postulation (created=True).
        2. Se obtiene la Petition asociada mediante id_petition.
        3. Se obtiene el Customer vinculado a la petición.
        4. Se envía una notificación al usuario del cliente usando notification_service.
    """
    if created:
        try:
            petition = Petition.objects.get(pk=instance.id_petition_id)
            id_customer = petition.id_customer
            customer = Customer.objects.get(id_customer=id_customer)
            
            # Usar el servicio de notificaciones para envío en tiempo real
            notification_service.send_notification(
                user_id=customer.user.id_user,
                title="Nueva postulación recibida",
                message=f"Tu petición '{petition.description}' recibió una nueva postulación.",
                notification_type='postulation_created',
                related_postulation_id=instance.id_postulation, # Asumiendo que Notification espera un ID
                related_petition_id=instance.id_petition_id, # Usar el ID, no el objeto
                metadata={
                    'postulation_id': instance.id_postulation, # ID
                    'petition_id': instance.id_petition_id, # ID
                    'provider_id': instance.id_provider # ID
                }
            )
        except (Petition.DoesNotExist, Customer.DoesNotExist):
            return

# ====================================================
# SIGNAL: notify_on_state_change
# ====================================================
@receiver(pre_save, sender=Postulation)
def notify_on_state_change(sender, instance, **kwargs):
    """
    Señal que se ejecuta antes de guardar una postulación existente (pre_save).
    Objetivo:
        → Detectar cambios en el estado de la postulación (id_state).
        → Notificar al proveedor (Provider) sobre el cambio.
    Flujo:
        1. Se compara el estado anterior con el nuevo.
        2. Si hay un cambio, se envía una notificación al proveedor.
        3. El tipo y contenido del mensaje dependen del nuevo estado:
            - 'Aceptada' → notificación de aceptación.
            - 'Rechazada' → notificación de rechazo.
            - Otro → notificación genérica de cambio de estado.
    """
    if not instance.pk:
        return  # no existe aún, no hay estado previo
    
    try:
        old_instance = Postulation.objects.get(pk=instance.pk)
    except Postulation.DoesNotExist:
        return
    
    if old_instance.id_state_id != instance.id_state_id:
        # El estado cambió
        try:
            provider = Provider.objects.get(id_provider=instance.id_provider)
            petition = Petition.objects.get(pk=instance.id_petition_id)
            
            # Determinar el tipo de notificación según el nuevo estado
            notification_type = 'postulation_state_changed'
            title = "Actualización de tu postulación"
            message = f"El estado de tu postulación para '{petition.description}' cambió de '{old_instance.id_state}' a '{instance.id_state}'."
            
            # Si el estado es "aceptada" o "rechazada", usar tipos específicos
            if instance.id_state.name.lower() in ['aceptada', 'aceptado', 'approved']:
                notification_type = 'postulation_accepted'
                title = "¡Postulación aceptada!"
                message = f"Tu postulación para '{petition.description}' ha sido aceptada."
            elif instance.id_state.name.lower() in ['rechazada', 'rechazado', 'rejected']:
                notification_type = 'postulation_rejected'
                title = "Postulación rechazada"
                message = f"Tu postulación para '{petition.description}' ha sido rechazada."
            
            notification_service.send_notification(
                user_id=provider.user.id_user,
                title=title,
                message=message,
                notification_type=notification_type,
                related_postulation_id=instance.id_postulation, # ID
                related_petition_id=instance.id_petition_id, # Usar el ID
                metadata={
                    'postulation_id': instance.id_postulation, # ID
                    'petition_id': instance.id_petition_id, # ID
                    'old_state': str(old_instance.id_state),
                    'new_state': str(instance.id_state)
                }
            )
        except (Provider.DoesNotExist, Petition.DoesNotExist):
            return


# ====================================================
# SIGNAL: notify_on_postulation_winner
# ====================================================
@receiver(post_save, sender=Postulation)
def notify_on_postulation_winner(sender, instance, **kwargs):
    """
    Señal que se ejecuta luego de guardar una postulación (post_save).
    Objetivo:
        → Notificar al proveedor cuando su postulación es marcada como ganadora.
    Flujo:
        1. Se verifica si el campo 'winner' está en True.
        2. Se obtiene el proveedor y la petición asociados.
        3. Se envía una notificación de tipo 'postulation_accepted'.
        4. Se marca la instancia temporalmente como notificada (_winner_notified)
           para evitar duplicados en ejecuciones múltiples del signal.
    """
    if instance.winner and not getattr(instance, '_winner_notified', False):
        try:
            provider = Provider.objects.get(id_provider=instance.id_provider)
            petition = Petition.objects.get(pk=instance.id_petition_id)
            
            notification_service.send_notification(
                user_id=provider.id_user,
                title="¡Felicidades! Has sido seleccionado",
                message=f"Tu postulación para '{petition.description}' ha sido seleccionada como ganadora.",
                notification_type='postulation_accepted',
                related_postulation_id=instance.id_postulation, # ID
                related_petition_id=instance.id_petition_id, # Usar el ID
                metadata={
                    'postulation_id': instance.id_postulation, # ID
                    'petition_id': instance.id_petition_id, # ID
                    'is_winner': True
                }
            )
            
            # Marcar como notificado para evitar duplicados
            instance._winner_notified = True
            
        except (Provider.DoesNotExist, Petition.DoesNotExist):
            return