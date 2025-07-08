from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def  create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('enabled', True)
        """
            aca puedo agregar flags: is_staff, is_superuser
        """
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    id_user = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    enabled = models.BooleanField(default=True)

    username = None # Eliminamos el campo username del modelo original

    USERNAME_FIELD = 'email'  # Campo que se usará para hacer login
    REQUIRED_FIELDS = [] # Campos requeridos al crear superusuario


    objects = UserManager() # Manager personalizado

    class Meta:
        db_table = 'user' # Apunta a la tabla ya existente
        managed = False  # Django no gestionará migraciones sobre esta tabla

    def __str__(self):
        return self.email