from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

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
        print(f"EmailBackend: Intentando autenticar al usuario con email: {email}")
        if email is None or password is None:
            print("EmailBackend: No se proporcionó email o contraseña.")
            return None
        try:
            user = UserModel.objects.get(email=email)
            print(f"EmailBackend: Usuario encontrado: {user}")
        except UserModel.DoesNotExist:
            print("EmailBackend: Usuario no encontrado en la base de datos.")
            return None

        print("EmailBackend: Verificando contraseña...")
        if user.check_password(password):
            print("EmailBackend: La contraseña es correcta.")
            if self.user_can_authenticate(user):
                print("EmailBackend: El usuario puede autenticarse.")
                return user
            else:
                print("EmailBackend: El usuario no puede autenticarse (is_active=False).")
        else:
            print("EmailBackend: La contraseña es incorrecta.")

        return None
