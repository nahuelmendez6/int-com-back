"""
Configuración de URLs principal del proyecto **integracion_comunitaria**.

Este archivo define el enrutamiento global de la aplicación, conectando las URLs
principales del proyecto con las URLConfs de cada aplicación interna.

Más información:
https://docs.djangoproject.com/en/5.2/topics/http/urls/

Ejemplos:
    - Funciones basadas en vistas:
        from my_app import views
        path('', views.home, name='home')
    - Vistas basadas en clases:
        from other_app.views import Home
        path('', Home.as_view(), name='home')
    - Inclusión de otras URLConfs:
        from django.urls import include, path
        path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


# -----------------------------------------------------------
# URLPATTERNS PRINCIPALES
# -----------------------------------------------------------
# Cada entrada en esta lista asocia una URL base con las rutas internas
# definidas en las aplicaciones del proyecto.
urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('authentication.urls')),

    path('locations/', include('locations.urls')),
    path('profiles/', include('profiles.urls')),

    path('availability/', include('availability.urls')),

    path('petitions/', include('petitions.urls')),

    path('offers/', include('offers.urls')),

    path('interests/', include('interest.urls')),

    path('postulations/', include('postulations.urls')),

    path('portfolios/', include('portfolio.urls')),

    path('api/contrataciones/', include('hires.urls')),

    path('grades/', include('grades.urls')),
    
    path('notifications/', include('notifications.urls')),

    path('api/chat/', include('chat.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 