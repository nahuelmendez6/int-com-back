from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



from locations.models import Address
from profiles.models import Category, TypeProvider, Profession
from .models import User, Customer, Provider


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
    lastname = serializers.CharField()
    role = serializers.ChoiceField(choices=[('customer', 'Cliente'), ('provider', 'Proveedor')])

    # Datos opcionales de cliente
    dni = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), required=False)

    # Datos opcionales de proveedor
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, many=True)
    type_provider = serializers.PrimaryKeyRelatedField(queryset=TypeProvider.objects.all(), required=False)
    profession = serializers.PrimaryKeyRelatedField(queryset=Profession.objects.all(), required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'lastname', 'role', 'dni', 'phone', 'address', 'categories',
                  'type_provider', 'profession', 'description']

    def validate(self, data):
        role = data.get('role')
        if role == 'customer':
            #if not data.get('address'):
            #    raise serializers.ValidationError('Direccion obligatoria para cliente')
            required_fields = ['email', 'password', 'name', 'lastname', 'dni', 'phone']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f'{field} es obligatorio')

        elif role == 'provider':
            required_fields = ['email', 'password', 'name', 'lastname']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f'{field} es obligatorio')

        else:
            raise serializers.ValidationError('Rol inválido o no especificado')

        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        name = validated_data.pop('name')
        lastname = validated_data.pop('lastname')
        categories_data = validated_data.pop('categories', [])

        user = User.objects.create_user(email=email, password=password, name=name, lastname=lastname)

        if role == 'customer':
            Customer.objects.create(
                user=user,
                dni=validated_data.get('dni'),
                phone=validated_data.get('phone'),
                address=validated_data.get('address')
            )
        elif role == 'provider':
            provider = Provider.objects.create(
                user=user,
                type_provider=validated_data.get("type_provider"),
                profession=validated_data.get("profession"),
                address=validated_data.get("address"),
                description=validated_data.get("description", "")
            )
            if categories_data:
                provider.categories.set(categories_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            raise serializers.ValidationError('Email y contraseña son requeridos.')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError('Credenciales inválidas.')

        if not user.enabled:
            raise serializers.ValidationError('Usuario deshabilitado.')

        refresh = RefreshToken.for_user(user)

        # Obtener rol
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