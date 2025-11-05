"""
Configuración WSGI para el proyecto **integracion_comunitaria**.

Este archivo define la interfaz WSGI (Web Server Gateway Interface),
que actúa como punto de entrada entre el servidor web (como Gunicorn o uWSGI)
y la aplicación Django.

WSGI es el estándar utilizado para desplegar aplicaciones Python en servidores web.

Más información:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# -----------------------------------------------------------
# CONFIGURACIÓN DEL MÓDULO DE SETTINGS DE DJANGO
# -----------------------------------------------------------
# Se define la variable de entorno que indica a Django qué archivo de configuración usar.
# En este caso, apunta al módulo principal de configuración del proyecto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integracion_comunitaria.settings')



# -----------------------------------------------------------
# INSTANCIACIÓN DE LA APLICACIÓN WSGI
# -----------------------------------------------------------
# `get_wsgi_application()` devuelve un objeto WSGI que será utilizado por el servidor web
# para enrutar las solicitudes HTTP a la aplicación Django.
#
# Este objeto `application` es reconocido por servidores WSGI como:
# - Gunicorn
# - uWSGI
# - mod_wsgi (Apache)
#
# Es el punto de entrada oficial para servir la aplicación en producción.
application = get_wsgi_application()
