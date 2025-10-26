from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



from locations.models import Address
from locations.serializers import AddressSerializer
from profiles.models import Category, TypeProvider, Profession
from .models import User, Customer, Provider, UserVerificationCode

# ====================================
# SERIALIZER DE REGISTRO DE USUARIO
# ====================================
class RegisterSerializer(serializers.ModelSerializer):

    """
    Serializer utilizado para el registro de nuevos usuarios.
    Permite crear tanto clientes como proveedores en base al rol seleccionado.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
    lastname = serializers.CharField()
    role = serializers.ChoiceField(choices=[('customer', 'Cliente'), ('provider', 'Proveedor')])

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'lastname', 'role']

    def validate_role(self, value):

        """
        Valida que el rol ingresado sea válido ('customer' o 'provider').
        """
        if value not in ['customer', 'provider']:
            raise serializers.ValidationError('Rol inválido')
        return value

    def create(self, validated_data):

        """
        Crea un usuario con el rol correspondiente (cliente o proveedor).
        También inicializa su instancia relacionada en el modelo respectivo.

        Args:
            validated_data (dict): Datos validados del formulario de registro.

        Returns:
            User: Instancia del usuario creado.
        """
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            email=validated_data['email'],
            password=password,
            name=validated_data['name'],
            lastname=validated_data['lastname'],
            is_active=True
        )

        # Asociar al tipo de perfil correspondiente
        if role == 'customer':
            Customer.objects.create(user=user)
        elif role == 'provider':
            Provider.objects.create(user=user)

        # Generar y enviar código de verificación
        # generate_verification_code(user)

        return user


# ====================================
# SERIALIZER DE LOGIN
# ====================================
class LoginSerializer(serializers.Serializer):

    """
    Serializer encargado de manejar la autenticación de usuarios.
    Verifica credenciales, genera tokens JWT y retorna información del usuario autenticado.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        """
        Valida las credenciales del usuario y genera los tokens de acceso.

        Raises:
            serializers.ValidationError: Si las credenciales son inválidas o el usuario está deshabilitado.

        Returns:
            dict: Datos del usuario autenticado, incluyendo tokens y rol.
        """

        email = data.get('email')
        password = data.get('password')

        print("🔍 Intentando autenticación con:")
        print(f"Email: {email}")
        print(f"Password: {password}")

        user = authenticate(email=email, password=password)
        print("Resultado de authenticate:", user)

        if not user:
            raise serializers.ValidationError('Credenciales inválidas.')

        if not user.is_active:
            raise serializers.ValidationError('Usuario deshabilitado.')

        refresh = RefreshToken.for_user(user)

        role = None
        if hasattr(user, 'customer'):
            role = 'customer'
        elif hasattr(user, 'provider'):
            role = 'provider'
        else:
            role = 'admin' if user.is_staff else 'user'

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": role,
            "user_id": user.id_user,
            "email": user.email,
        }

# ====================================
# SERIALIZER BÁSICO DE USUARIO
# ====================================
class UserSerializer(serializers.ModelSerializer):

    """
    Serializer simplificado para representar información básica del usuario.
    """

    class Meta:
        model = User
        fields = ['id_user', 'name', 'lastname', 'email', 'profile_image']


# ====================================
# SERIALIZER DE LECTURA DE PROVEEDOR
# ====================================
class ProviderReadSerializer(serializers.ModelSerializer):

    """
    Serializer utilizado para mostrar la información completa de un proveedor.
    Incluye relaciones con usuario, categorías, ciudades, profesión, etc.
    """
    user = UserSerializer()
    type_provider = serializers.StringRelatedField()
    profession = serializers.StringRelatedField()
    address = serializers.StringRelatedField()
    categories = serializers.StringRelatedField(many=True)
    cities = serializers.StringRelatedField()

    class Meta:
        model = Provider
        fields = [
            'id_provider',
            'user',
            'type_provider',
            'profession',
            'address',
            'description',
            'categories',
            'cities'
        ]


# ====================================
# SERIALIZER DE EDICIÓN / CREACIÓN DE PROVEEDOR
# ====================================
class ProviderSerializer(serializers.ModelSerializer):

        """
        Serializer utilizado para la creación o actualización de datos
        de un proveedor, incluyendo la asociación con categorías.
        """

        categories = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Category.objects.all()
        )

        class Meta:
            model = Provider
            fields = '__all__'


# ====================================
# SERIALIZER DE PERFIL DE USUARIO
# ====================================
class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer que retorna la información del perfil del usuario logueado,
    incluyendo una URL absoluta de la imagen de perfil.
    """
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['name', 'lastname', 'email', 'profile_image']

    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            return request.build_absolute_uri(obj.profile_image.url)
        return None
