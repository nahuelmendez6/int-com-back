from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

from profiles.models import Category

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
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    #password = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    date_update = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)


    username = None # Eliminamos el campo username del modelo original
    first_name = None
    last_name = None

    # Campos requeridos por Django Admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager() # Manager personalizado

    USERNAME_FIELD = 'email'  # Campo que se usará para hacer login
    REQUIRED_FIELDS = []  # Campos requeridos al crear superusuario

    class Meta:
        db_table = 'n_user' # Apunta a la tabla ya existente
        managed = False  # Django no gestionará migraciones sobre esta tabla

    def __str__(self):
        return self.email


class Customer(models.Model):

    id_customer = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE, db_column='user_id', related_name='customer'
    )
    dni = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.ForeignKey(
        'locations.Address', on_delete=models.SET_NULL, null=True, db_column='address_id',
        related_name='customer_addresses'
    )

    class Meta:
        db_table = 'n_customer'
        managed = False

    def __str__(self):
        return f"Cliente: {self.user.email}"


class Provider(models.Model):
    id_provider = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE, db_column='user_id', related_name='provider'
    )
    categories = models.ManyToManyField(
        'profiles.Category', through='ProviderCategory', related_name='providers'
    )
    type_provider = models.ForeignKey(
        'profiles.TypeProvider', on_delete=models.SET_NULL, null=True, db_column='id_type_provider', related_name='providers'
    )
    profession = models.ForeignKey(
        'profiles.Profession', on_delete=models.SET_NULL, null=True, db_column='id_profession', related_name='providers'
    )
    address = models.ForeignKey(
        'locations.Address', on_delete=models.SET_NULL, null=True, db_column='address_id', related_name='provider_addresses'
    )
    description = models.TextField(null=True, blank=True)

    # para que el proveedor pueda acceder directamente a sus ciudades
    cities = models.ManyToManyField(
        'locations.City',
        through='locations.ProviderCity',
        related_name='provider_set'
    )

    class Meta:
        db_table = 'n_provider'
        managed = False

    def __str__(self):
        return f"Proveedor: {self.user.email}"

    def is_profile_complete(self):
        has_categories = ProviderCategory.objects.filter(provider=self).exists()

        return all([
            self.type_provider is not None,
            self.profession is not None,
            self.address is not None,
            bool(self.description),
            has_categories,
            self.cities.exists()
        ])


class ProviderCategory(models.Model):
    id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, db_column='provider_id')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category_id')

    class Meta:
        db_table = 'n_provider_cateogory'  # escribilo tal como está en la base de datos
        unique_together = ('provider', 'category')


class UserVerificationCode(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id', related_name='verification_codes')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'n_user_verification_code'
        managed = False

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"Código {self.code} para {self.user.email}"