from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from notifications.models import Notification
from notifications.services import notification_service
from .models import Postulation
from petitions.models import Petition
from authentication.models import Customer, Provider

@receiver(post_save, sender=Postulation)
def notify_on_postulation_create(sender, instance, created, **kwargs):
    """
    Notificar al customer cuando se crea una nueva postulación
    """
    if created:
        try:
            petition = Petition.objects.get(pk=instance.id_petition)
            id_customer = petition.id_customer
            customer = Customer.objects.get(id_customer=id_customer)
            
            # Usar el servicio de notificaciones para envío en tiempo real
            notification_service.send_notification(
                user_id=customer.user.id_user,
                title="Nueva postulación recibida",
                message=f"Tu petición '{petition.description}' recibió una nueva postulación.",
                notification_type='postulation_created',
                related_postulation_id=instance.id_postulation,
                related_petition_id=instance.id_petition,
                metadata={
                    'postulation_id': instance.id_postulation,
                    'petition_id': instance.id_petition,
                    'provider_id': instance.id_provider
                }
            )
        except (Petition.DoesNotExist, Customer.DoesNotExist):
            return

@receiver(pre_save, sender=Postulation)
def notify_on_state_change(sender, instance, **kwargs):
    """
    Notificar al provider cuando cambia el estado de su postulación
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
            petition = Petition.objects.get(pk=instance.id_petition)
            
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
                related_postulation_id=instance.id_postulation,
                related_petition_id=instance.id_petition,
                metadata={
                    'postulation_id': instance.id_postulation,
                    'petition_id': instance.id_petition,
                    'old_state': str(old_instance.id_state),
                    'new_state': str(instance.id_state)
                }
            )
        except (Provider.DoesNotExist, Petition.DoesNotExist):
            return

@receiver(post_save, sender=Postulation)
def notify_on_postulation_winner(sender, instance, **kwargs):
    """
    Notificar cuando una postulación es marcada como ganadora
    """
    if instance.winner and not getattr(instance, '_winner_notified', False):
        try:
            provider = Provider.objects.get(id_provider=instance.id_provider)
            petition = Petition.objects.get(pk=instance.id_petition)
            
            notification_service.send_notification(
                user_id=provider.id_user,
                title="¡Felicidades! Has sido seleccionado",
                message=f"Tu postulación para '{petition.description}' ha sido seleccionada como ganadora.",
                notification_type='postulation_accepted',
                related_postulation_id=instance.id_postulation,
                related_petition_id=instance.id_petition,
                metadata={
                    'postulation_id': instance.id_postulation,
                    'petition_id': instance.id_petition,
                    'is_winner': True
                }
            )
            
            # Marcar como notificado para evitar duplicados
            instance._winner_notified = True
            
        except (Provider.DoesNotExist, Petition.DoesNotExist):
            return