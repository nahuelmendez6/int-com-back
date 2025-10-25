#!/usr/bin/env python
"""
Script de configuración para desarrollo
Ejecutar con: python manage.py shell < notifications/development_setup.py
"""

from django.contrib.auth.models import User
from notifications.models import NotificationSettings
from authentication.models import Customer, Provider

def setup_development_environment():
    """Configura el entorno de desarrollo con datos de prueba"""
    
    print("🔧 Configurando entorno de desarrollo...")
    
    # Crear usuarios de desarrollo si no existen
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'customer1',
            'email': 'customer1@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez'
        },
        {
            'username': 'provider1',
            'email': 'provider1@test.com',
            'first_name': 'María',
            'last_name': 'González'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password('test123')
            user.save()
            print(f"✅ Usuario creado: {user.username}")
        else:
            print(f"ℹ️ Usuario ya existe: {user.username}")
        created_users.append(user)
    
    # Crear perfiles de Customer y Provider
    print("\n👥 Creando perfiles...")
    
    # Customer
    customer_user = User.objects.get(username='customer1')
    customer, created = Customer.objects.get_or_create(
        id_user=customer_user,
        defaults={'id_customer': 1, 'is_active': True}
    )
    if created:
        print(f"✅ Customer creado: {customer_user.username}")
    else:
        print(f"ℹ️ Customer ya existe: {customer_user.username}")
    
    # Provider
    provider_user = User.objects.get(username='provider1')
    provider, created = Provider.objects.get_or_create(
        id_user=provider_user,
        defaults={'id_provider': 1, 'is_active': True}
    )
    if created:
        print(f"✅ Provider creado: {provider_user.username}")
    else:
        print(f"ℹ️ Provider ya existe: {provider_user.username}")
    
    # Configurar notificaciones para todos los usuarios
    print("\n🔔 Configurando notificaciones...")
    
    for user in created_users:
        settings, created = NotificationSettings.objects.get_or_create(
            user=user,
            defaults={
                'postulation_created': True,
                'postulation_state_changed': True,
                'postulation_accepted': True,
                'postulation_rejected': True,
                'petition_closed': True,
                'email_notifications': True,
                'push_notifications': True
            }
        )
        if created:
            print(f"✅ Configuración creada para: {user.username}")
        else:
            print(f"ℹ️ Configuración ya existe para: {user.username}")
    
    print("\n🎉 ¡Entorno de desarrollo configurado!")
    print("\n📋 Credenciales de prueba:")
    print("👤 Admin: admin / test123")
    print("👤 Customer: customer1 / test123")
    print("👤 Provider: provider1 / test123")
    print("\n🔗 URLs importantes:")
    print("- Admin: http://localhost:8000/admin/")
    print("- API Notificaciones: http://localhost:8000/notifications/")
    print("- WebSocket: ws://localhost:8000/ws/notifications/{user_id}/")
    print("\n📚 Documentación:")
    print("- README.md: Información general del sistema")
    print("- FRONTEND_INTEGRATION.md: Guía de integración frontend")
    print("- test_notifications.py: Script de pruebas")

if __name__ == "__main__":
    setup_development_environment()
