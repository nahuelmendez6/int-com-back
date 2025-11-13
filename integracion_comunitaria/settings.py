"""
Configuración principal del proyecto Django **integracion_comunitaria**.

Este archivo contiene todos los ajustes esenciales para el funcionamiento
del proyecto, incluyendo:
    - Configuración general y de seguridad.
    - Aplicaciones instaladas.
    - Middleware.
    - Base de datos.
    - Autenticación y JWT.
    - Canales (WebSockets).
    - Configuración de Celery + Redis.
    - Configuración de correo (SMTP).
    - Archivos estáticos y multimedia.

Más información:
https://docs.djangoproject.com/en/5.2/topics/settings/
"""
from email.policy import default

from decouple import config

from pathlib import Path

import os

from datetime import timedelta

# -----------------------------------------------------------
# RUTAS BASE DEL PROYECTO
# -----------------------------------------------------------
# Define la ruta base del proyecto (utilizada para construir rutas relativas)
BASE_DIR = Path(__file__).resolve().parent.parent


# -----------------------------------------------------------
# CONFIGURACIONES DE SEGURIDAD
# -----------------------------------------------------------
# Clave secreta de Django (mantener privada en producción)
SECRET_KEY = config('SECRET_KEY')

# Activa o desactiva el modo de depuración (no usar en producción)
DEBUG = config('DEBUG', default=False, cast=bool)

# Define los dominios permitidos que pueden acceder a la aplicación
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: v.split(','))


# -----------------------------------------------------------
# APLICACIONES INSTALADAS
# -----------------------------------------------------------

INSTALLED_APPS = [
    # Apps principales de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librerías externas
    'corsheaders',
    'debug_toolbar',

    'rest_framework',
    'rest_framework_simplejwt',
    'channels',

    # Aplicaciones del proyecto
    'authentication',
    'locations',
    'profiles',
    'availability',
    'petitions',
    'offers',
    'interest',
    'postulations',
    'portfolio',
    'hires',
    'grades',
    'notifications',
    'chat',

]

# -----------------------------------------------------------
# CONFIGURACIÓN DE ASGI Y CANALES (WebSockets)
# -----------------------------------------------------------
ASGI_APPLICATION = "integracion_comunitaria.asgi.application"

# Configuración de capas de canales usando Redis como backend
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# -----------------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    "127.0.0.1",
]



# -----------------------------------------------------------
# CONFIGURACIÓN DE DJANGO REST FRAMEWORK
# -----------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

}

# -----------------------------------------------------------
# CONFIGURACIÓN DE URLS Y TEMPLATES
# -----------------------------------------------------------
ROOT_URLCONF = 'integracion_comunitaria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Aplicación WSGI (para servidores tradicionales)
WSGI_APPLICATION = 'integracion_comunitaria.wsgi.application'



# -----------------------------------------------------------
# CONFIGURACIÓN DE LOGGING
# -----------------------------------------------------------
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
"""

# -----------------------------------------------------------
# BASE DE DATOS
# -----------------------------------------------------------
# Configuración de conexión (se lee desde variables de entorno .env)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
    }
}


# -----------------------------------------------------------
# VALIDADORES DE CONTRASEÑAS
# -----------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# -----------------------------------------------------------
# CONFIGURACIÓN DE INTERNACIONALIZACIÓN
# -----------------------------------------------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# -----------------------------------------------------------
# ARCHIVOS ESTÁTICOS Y MULTIMEDIA
# -----------------------------------------------------------

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------
# CONFIGURACIÓN DE MODELOS Y AUTENTICACIÓN
# -----------------------------------------------------------
# Modelo de usuario personalizado

AUTH_USER_MODEL = 'authentication.User' # la entidad User de la app auth es la que maneja la autenticacion de usuario
# Backends de autenticación (por correo o por username)
AUTHENTICATION_BACKENDS = [
    'authentication.backends.EmailBackend',
'django.contrib.auth.backends.ModelBackend',
]

# -----------------------------------------------------------
# CONFIGURACIÓN DE TOKENS JWT
# -----------------------------------------------------------
SIMPLE_JWT = {
    'USER_ID_FIELD': 'id_user',
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),  # duración del access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # duración del refresh token
    'ROTATE_REFRESH_TOKENS': True,                # opcional: crea nuevos tokens al refrescar
    'BLACKLIST_AFTER_ROTATION': True,             # invalida los viejos
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# -----------------------------------------------------------
# CONFIGURACIÓN DE CORS (acceso desde frontend)
# -----------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True



DEBUG = True

# -----------------------------------------------------------
# CONFIGURACIÓN DE CELERY + REDIS
# -----------------------------------------------------------
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


# -----------------------------------------------------------
# CONFIGURACIÓN DE EMAIL (SMTP)
# -----------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # u otro
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'integracioncomunitaria2025@gmail.com'
EMAIL_HOST_PASSWORD = 'live qfdp txew asuq '
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
    'console': {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    },
    },
   'loggers': {
   'django.db.backends': {
   'handlers': ['console'],
   'level': 'DEBUG',
   },
   },
}
"""