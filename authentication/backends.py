import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
logger = logging.getLogger(__name__)

# Se obtiene el modelo de usuario activo definido en la configuración del proyecto
UserModel = get_user_model()


# ====================================
# BACKEND DE AUTENTICACIÓN PERSONALIZADO
# ====================================
class EmailBackend(ModelBackend):

    """
    Backend de autenticación personalizado que permite el inicio de sesión
    utilizando el campo 'email' en lugar del 'username' por defecto de Django.
    
    Este backend se integra con el sistema de autenticación estándar de Django,
    validando las credenciales del usuario y verificando su estado de activación.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):

        """
        Autentica un usuario basándose en su correo electrónico y contraseña.

        Args:
            request (HttpRequest): Objeto de la solicitud HTTP (puede ser None).
            username (str, opcional): Nombre de usuario; aquí se interpreta como email.
            password (str, opcional): Contraseña del usuario.
            **kwargs: Argumentos adicionales, como 'email'.

        Returns:
            User | None: Retorna la instancia del usuario si la autenticación es exitosa,
                         o None si falla la validación.
        """


        email = kwargs.get('email') or username
        logger.debug(f"EmailBackend: Intentando autenticar al usuario con email: {email}")
        if email is None or password is None:
            logger.warning("EmailBackend: No se proporcionó email o contraseña.")
            return None
        try:
            user = UserModel.objects.get(email=email)
            logger.debug(f"EmailBackend: Usuario encontrado: {user}")
        except UserModel.DoesNotExist:
            logger.info(f"EmailBackend: Usuario con email {email} no encontrado en la base de datos.")
            return None

        logger.debug("EmailBackend: Verificando contraseña...")
        if user.check_password(password):
            logger.debug("EmailBackend: La contraseña es correcta.")
            if self.user_can_authenticate(user):
                logger.debug("EmailBackend: El usuario puede autenticarse.")
                return user
            else:
                logger.warning(f"EmailBackend: El usuario {email} no puede autenticarse (is_active=False).")
        else:
            logger.warning(f"EmailBackend: La contraseña para el usuario {email} es incorrecta.")

        return None
