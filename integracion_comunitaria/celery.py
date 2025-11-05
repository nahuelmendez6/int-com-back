"""
Configuración principal de Celery para el proyecto **integracion_comunitaria**.

Celery es un sistema de procesamiento de tareas en segundo plano (asíncronas)
que permite ejecutar funciones fuera del flujo principal de Django,
ideal para operaciones como envío de correos, notificaciones o procesamiento intensivo.

Este archivo inicializa la aplicación Celery, carga la configuración desde Django
y autodetecta las tareas definidas en los módulos del proyecto.

Más información:
https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""

import os
from celery import Celery


# Establece el módulo de configuración de Django predeterminado
# para que Celery pueda acceder a las configuraciones del proyecto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integracion_comunitaria.settings')

# Crea una instancia de la aplicación Celery con el nombre del proyecto
app = Celery('integracion_comunitaria')


# Configura Celery para cargar sus ajustes desde el archivo de configuración de Django
# utilizando el prefijo "CELERY_" en las variables (por ejemplo: CELERY_BROKER_URL).
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodescubre automáticamente todas las tareas definidas en los módulos "tasks.py"
# dentro de las aplicaciones registradas en INSTALLED_APPS.
app.autodiscover_tasks()

