from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
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
