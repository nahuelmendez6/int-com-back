# Integración Comunitaria Backend

Este proyecto es el backend de una aplicación de "Integración Comunitaria", desarrollado con Django y Django REST Framework. Proporciona una API robusta para gestionar usuarios, perfiles, ubicaciones y autenticación, con soporte para tareas asíncronas utilizando Celery.

## Estructura del Proyecto

El proyecto está organizado en las siguientes aplicaciones principales:

-   **`authentication/`**: Gestiona todo lo relacionado con la autenticación de usuarios, incluyendo registro, inicio de sesión, gestión de tokens, y posiblemente recuperación de contraseñas. Incluye modelos de usuario, serializadores, vistas, servicios y tareas asíncronas.
-   **`profiles/`**: Maneja los perfiles de usuario, extendiendo el modelo de usuario base con información adicional. Contiene modelos, serializadores y vistas para la gestión de perfiles.
-   **`locations/`**: Administra la información de ubicaciones, que podría estar asociada a usuarios, eventos o recursos. Incluye modelos, serializadores y vistas para la gestión de ubicaciones.
-   **`integracion_comunitaria/`**: Es el directorio principal del proyecto Django, donde se encuentran la configuración global (`settings.py`), las URLs principales (`urls.py`), y la configuración de Celery (`celery.py`).

## Funcionalidades Clave

-   **Autenticación de Usuarios**: Sistema completo de registro y login, probablemente basado en tokens (JWT u OAuth2).
-   **Gestión de Perfiles**: Creación y actualización de perfiles de usuario con información detallada.
-   **Gestión de Ubicaciones**: CRUD (Crear, Leer, Actualizar, Eliminar) para entidades de ubicación.
-   **API RESTful**: Todas las funcionalidades se exponen a través de una API RESTful, facilitando la integración con clientes frontend.
-   **Tareas Asíncronas**: Utilización de Celery para ejecutar tareas en segundo plano, como el envío de correos electrónicos, procesamiento de imágenes o notificaciones, mejorando la responsividad de la aplicación.

## Tecnologías Utilizadas

-   **Django**: Framework web para el desarrollo rápido y seguro.
-   **Django REST Framework**: Para la construcción de APIs RESTful.
-   **Celery**: Procesador de tareas distribuidas para operaciones asíncronas.
-   **PostgreSQL (asumido)**: Base de datos relacional (comúnmente utilizada con Django).
-   **Redis (asumido)**: Broker de mensajes para Celery.

## Configuración y Ejecución

(Se añadirán instrucciones detalladas sobre cómo configurar el entorno, instalar dependencias, ejecutar migraciones y levantar el servidor en futuras actualizaciones de este README.)
