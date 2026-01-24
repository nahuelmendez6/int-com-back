# Integración Comunitaria - Backend

Este proyecto constituye el backend de la plataforma "Integración Comunitaria", una aplicación diseñada para conectar proveedores de servicios con clientes mediante un sistema robusto de peticiones, postulaciones y comunicación en tiempo real.

El sistema está construido sobre **Django** y **Django REST Framework**, implementando una arquitectura escalable que incluye tareas asíncronas y WebSockets.

## 🚀 Tecnologías y Stack

*   **Lenguaje**: Python 3.x
*   **Framework Web**: Django 5.x
*   **API REST**: Django REST Framework (DRF)
*   **Base de Datos**: MySQL
*   **Asincronía y Colas**: Celery + Redis
*   **Tiempo Real (WebSockets)**: Django Channels + Redis
*   **Autenticación**: JWT (JSON Web Tokens) con `djangorestframework-simplejwt`

## 📂 Arquitectura y Módulos

El proyecto está organizado en aplicaciones desacopladas para facilitar el mantenimiento:

*   **`authentication`**: Manejo de usuarios (modelo personalizado `User`), autenticación vía email, y gestión de tokens JWT.
*   **`profiles`**: Gestión de perfiles extendidos (`Provider` y `Customer`). Incluye lógica para dashboards y catálogos (Categorías, Profesiones).
*   **`petitions`**: Núcleo del sistema. Permite a los clientes crear solicitudes de servicio (con adjuntos y materiales) y a los proveedores visualizarlas según su rubro.
*   **`postulations`**: Gestión del ciclo de vida de una postulación y estadísticas de rendimiento para proveedores.
*   **`chat`**: Sistema de mensajería instantánea entre cliente y proveedor para negociar servicios.
*   **`locations`**: Normalización de direcciones geográficas (País, Provincia, Ciudad).
*   **`notifications`**: Sistema de alertas para los usuarios.
*   **`integracion_comunitaria`**: Configuración global del proyecto.

## ✨ Funcionalidades Principales

1.  **Dashboard Inteligente**:
    *   Endpoint unificado `/profiles/dashboard/` que adapta la respuesta según el rol (Cliente o Proveedor), mostrando métricas clave, estados de peticiones y alertas.
2.  **Sistema de Peticiones**:
    *   Filtrado automático: Los proveedores solo ven peticiones relevantes a su profesión y ubicación.
    *   Soporte para adjuntar imágenes y listas de materiales.
3.  **Estadísticas para Proveedores**:
    *   Análisis de postulaciones (ganadas, perdidas, pendientes) para mejorar la competitividad del proveedor.
4.  **Chat en Tiempo Real**:
    *   Comunicación fluida integrada en la plataforma, respaldada por WebSockets.
5.  **Seguridad**:
    *   Validación de roles y permisos a nivel de endpoint.
    *   Autenticación segura mediante Bearer Tokens.

## 🛠️ Guía de Instalación y Ejecución

Sigue estos pasos para levantar el entorno de desarrollo.

### 1. Prerrequisitos
Asegúrate de tener instalado:
*   Python 3.10 o superior
*   MySQL Server
*   Redis Server (Requerido para Celery y el Chat)

### 2. Configuración del Entorno

Clona el repositorio y crea tu entorno virtual:

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Activar entorno (Windows)
venv\Scripts\activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

### 3. Variables de Entorno (.env)

Crea un archivo `.env` en la raíz del proyecto (`/back/`) con las siguientes configuraciones. Estas son necesarias ya que el proyecto utiliza `python-decouple`:

```env
# Seguridad y Configuración Django
SECRET_KEY=tu_clave_secreta_generada
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de Datos (MySQL)
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario_mysql
DB_PASSWORD=tu_password_mysql
DB_HOST=localhost
DB_PORT=3306
```

> **Nota:** La configuración de Email y Redis viene preconfigurada en `settings.py` para desarrollo, pero puede requerir ajustes en producción.

### 4. Base de Datos

Asegúrate de que tu servidor MySQL esté corriendo y la base de datos definida en el `.env` exista.

```bash
# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate
```

### 5. Ejecutar el Servidor

```bash
python manage.py runserver
```
La API estará disponible en `http://localhost:8000`.

### 6. Ejecutar Celery (Tareas en segundo plano)

Para que funcionen el envío de correos y otras tareas asíncronas, necesitas correr un worker de Celery en una terminal separada (con el entorno virtual activado):

```bash
celery -A integracion_comunitaria worker -l info
```

## 🔗 Endpoints Clave

Aquí tienes un resumen de las rutas más importantes:

| Módulo | Método | Endpoint | Descripción |
|--------|--------|----------|-------------|
| **Auth** | POST | `/api/token/` | Login (Obtener Token) |
| **Perfil** | GET | `/profiles/dashboard/` | Resumen de actividad |
| **Perfil** | GET | `/profiles/user/` | Datos del usuario y perfil |
| **Peticiones** | GET | `/petitions/` | Listar peticiones (filtrado por rol) |
| **Peticiones** | POST | `/petitions/` | Crear nueva petición |
| **Estadísticas**| GET | `/postulations/statistics/` | Métricas de proveedor |
| **Chat** | POST | `/api/chat/conversations/start/`| Iniciar conversación |

---
Desarrollado por el equipo de Integración Comunitaria.
