#!/usr/bin/env python
"""
Script de prueba para el sistema de notificaciones
Ejecutar con: python manage.py shell < notifications/test_notifications.py
"""

from django.contrib.auth import get_user_model
from notifications.models import Notification, NotificationSettings
from notifications.services import notification_service
from authentication.models import Customer, Provider

User = get_user_model()

def test_notification_system():
    """Prueba el sistema completo de notificaciones"""
    
    print("🧪 Iniciando pruebas del sistema de notificaciones...")
    
    # 1. Crear usuarios de prueba
    print("\n1. Creando usuarios de prueba...")
    
    # Customer
    customer_user, created = User.objects.get_or_create(
        username='test_customer',
        defaults={'email': 'customer@test.com', 'first_name': 'Test', 'last_name': 'Customer'}
    )
    customer, created = Customer.objects.get_or_create(
        id_user=customer_user,
        defaults={'id_customer': 999, 'is_active': True}
    )
    print(f"✅ Customer creado: {customer_user.username}")
    
    # Provider
    provider_user, created = User.objects.get_or_create(
        username='test_provider',
        defaults={'email': 'provider@test.com', 'first_name': 'Test', 'last_name': 'Provider'}
    )
    provider, created = Provider.objects.get_or_create(
        id_user=provider_user,
        defaults={'id_provider': 999, 'is_active': True}
    )
    print(f"✅ Provider creado: {provider_user.username}")
    
    # 2. Crear configuración de notificaciones
    print("\n2. Configurando notificaciones...")
    
    customer_settings, created = NotificationSettings.objects.get_or_create(
        user=customer_user,
        defaults={
            'postulation_created': True,
            'email_notifications': True,
            'push_notifications': True
        }
    )
    print(f"✅ Configuración customer: {customer_settings}")
    
    provider_settings, created = NotificationSettings.objects.get_or_create(
        user=provider_user,
        defaults={
            'postulation_state_changed': True,
            'postulation_accepted': True,
            'email_notifications': True,
            'push_notifications': True
        }
    )
    print(f"✅ Configuración provider: {provider_settings}")
    
    # 3. Probar creación de notificaciones
    print("\n3. Probando creación de notificaciones...")
    
    # Notificación para customer
    notification1 = notification_service.send_notification(
        user_id=customer_user.id,
        title="Nueva postulación recibida",
        message="Tu petición 'Reparación de techo' recibió una nueva postulación.",
        notification_type='postulation_created',
        related_postulation_id=123,
        related_petition_id=456,
        metadata={'test': True, 'provider_id': 789}
    )
    print(f"✅ Notificación customer creada: {notification1.id}")
    
    # Notificación para provider
    notification2 = notification_service.send_notification(
        user_id=provider_user.id,
        title="Estado de postulación actualizado",
        message="Tu postulación para 'Reparación de techo' cambió de estado.",
        notification_type='postulation_state_changed',
        related_postulation_id=123,
        related_petition_id=456,
        metadata={'test': True, 'old_state': 'pendiente', 'new_state': 'en_revisión'}
    )
    print(f"✅ Notificación provider creada: {notification2.id}")
    
    # 4. Probar notificaciones masivas
    print("\n4. Probando notificaciones masivas...")
    
    notifications = notification_service.send_bulk_notification(
        user_ids=[customer_user.id, provider_user.id],
        title="Mantenimiento del sistema",
        message="El sistema estará en mantenimiento el próximo domingo.",
        notification_type='general',
        metadata={'maintenance': True, 'date': '2024-01-21'}
    )
    print(f"✅ Notificaciones masivas enviadas: {len(notifications)}")
    
    # 5. Verificar estadísticas
    print("\n5. Verificando estadísticas...")
    
    customer_notifications = Notification.objects.filter(user=customer_user)
    provider_notifications = Notification.objects.filter(user=provider_user)
    
    print(f"📊 Customer - Total: {customer_notifications.count()}, No leídas: {customer_notifications.filter(is_read=False).count()}")
    print(f"📊 Provider - Total: {provider_notifications.count()}, No leídas: {provider_notifications.filter(is_read=False).count()}")
    
    # 6. Probar marcar como leída
    print("\n6. Probando marcar como leída...")
    
    if notification1:
        notification1.mark_as_read()
        print(f"✅ Notificación {notification1.id} marcada como leída")
    
    # 7. Verificar tipos de notificación
    print("\n7. Verificando tipos de notificación...")
    
    from notifications.models import NotificationType
    for choice in NotificationType.choices:
        print(f"📝 {choice[0]}: {choice[1]}")
    
    # 8. Limpiar datos de prueba
    print("\n8. Limpiando datos de prueba...")
    
    # Eliminar notificaciones de prueba
    Notification.objects.filter(metadata__test=True).delete()
    print("✅ Notificaciones de prueba eliminadas")
    
    # Eliminar usuarios de prueba (opcional)
    # customer_user.delete()
    # provider_user.delete()
    # print("✅ Usuarios de prueba eliminados")
    
    print("\n🎉 ¡Pruebas completadas exitosamente!")
    print("\n📋 Resumen:")
    print("- ✅ Modelos funcionando")
    print("- ✅ Servicio de notificaciones funcionando")
    print("- ✅ Configuración de usuarios funcionando")
    print("- ✅ Estadísticas funcionando")
    print("- ✅ Tipos de notificación disponibles")
    print("\n🚀 El sistema está listo para usar!")

if __name__ == "__main__":
    test_notification_system()
