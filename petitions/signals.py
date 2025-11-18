from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from notifications.services import notification_service
from .models import Petition
from authentication.models import Customer, Provider



# ====================================================
# SIGNAL: notify_on_petition_created
# ====================================================
@receiver(post_save, sender=Petition)
def notify_on_petition_created(sender, instance, created, **kwargs):
    """
    Notificar a los proveedores cuando se crea una nueva petición.
    
    Se dispara automáticamente después de guardar una instancia de Petition.
    Solo se ejecuta si la petición es recién creada (created=True).
    """
    if created:
        print(f"✅ SIGNAL: 'notify_on_petition_created' disparado para la petición: '{instance.description}'")
        # Obtener todos los proveedores que podrían estar interesados
        # Por ahora, notificamos a todos los proveedores activos
        providers = Provider.objects.filter(is_active=True)
        providers = Provider.objects.filter(user__is_active=True)
        
        print(f"ℹ️ SIGNAL: Se notificarán a {len(providers)} proveedores.")
        for provider in providers:
            notification_service.send_notification(
                user_id=provider.user.id_user,
                title="Nueva petición disponible",
                message=f"Se ha publicado una nueva petición: '{instance.description}'",
                notification_type='petition_created',
                related_petition_id=instance.id_petition,
                metadata={
                    'petition_id': instance.id_petition,
                    'petition_description': instance.description,
                    'petition_type': 'new_petition'
                }
            )

# ====================================================
# SIGNAL: notify_on_petition_closed
# ====================================================
@receiver(pre_save, sender=Petition)
def notify_on_petition_closed(sender, instance, **kwargs):
    """
    Notificar cuando una petición se cierra.
    
    Se dispara antes de guardar una instancia de Petition.
    Compara el estado anterior de la petición para detectar cierre.
    """
    if instance.pk:  # Solo para peticiones existentes
        try:
            old_instance = Petition.objects.get(pk=instance.pk)
            
            # Verificar si la petición se está cerrando
            if old_instance.is_active and not instance.is_active:
                # Notificar al customer
                customer = Customer.objects.get(id_customer=instance.id_customer)
                notification_service.send_notification(
                    user_id=customer.user.id_user,
                    title="Petición cerrada",
                    message=f"Tu petición '{instance.title}' ha sido cerrada.",
                    notification_type='petition_closed',
                    related_petition_id=instance.id_petition,
                    metadata={
                        'petition_id': instance.id_petition,
                        'petition_title': instance.title,
                        'closure_reason': 'manual'
                    }
                )
                
                # Notificar a todos los proveedores que postularon
                from postulations.models import Postulation
                postulations = Postulation.objects.filter(
                    id_petition=instance.id_petition,
                    is_deleted=False
                )
                
                for postulation in postulations:
                    provider = Provider.objects.get(id_provider=postulation.id_provider)
                    notification_service.send_notification(
                        user_id=provider.user.id_user,
                        title="Petición cerrada",
                        message=f"La petición '{instance.title}' en la que postulaste ha sido cerrada.",
                        notification_type='petition_closed',
                        related_petition_id=instance.id_petition,
                        related_postulation_id=postulation.id_postulation,
                        metadata={
                            'petition_id': instance.id_petition,
                            'postulation_id': postulation.id_postulation,
                            'petition_title': instance.title
                        }
                    )
                    
        except (Petition.DoesNotExist, Customer.DoesNotExist, Provider.DoesNotExist):
            return
